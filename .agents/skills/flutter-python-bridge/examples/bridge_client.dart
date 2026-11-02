import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

/// Dart WebSocket client managing communication with the Python Core Service.
class GameBridgeClient {
  static const String serverUrl = 'ws://127.0.0.1:8765/ws';
  
  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  Process? _pythonProcess;

  final ValueNotifier<Map<String, dynamic>?> gameState = ValueNotifier(null);
  final ValueNotifier<bool> isConnected = ValueNotifier(false);
  final StreamController<Map<String, dynamic>> _eventsController =
      StreamController.broadcast();

  Stream<Map<String, dynamic>> get eventsStream => _eventsController.stream;

  /// Starts Python backend process if not already running and connects WebSocket.
  Future<void> initialize() async {
    await _ensurePythonBackendRunning();
    await _connectWebSocket();
  }

  Future<void> _ensurePythonBackendRunning() async {
    try {
      final socket = await Socket.connect('127.0.0.1', 8765,
          timeout: const Duration(milliseconds: 500));
      await socket.close();
      debugPrint('[Bridge] Python backend already active on 8765.');
    } catch (_) {
      debugPrint('[Bridge] Spawning Python backend process...');
      _pythonProcess = await Process.start(
        'python3',
        ['backend/server.py'],
        workingDirectory: Directory.current.path,
      );
      // Wait for server to bind
      await Future.delayed(const Duration(seconds: 1));
    }
  }

  Future<void> _connectWebSocket() async {
    try {
      _channel = WebSocketChannel.connect(Uri.parse(serverUrl));
      _subscription = _channel!.stream.listen(
        _onMessageReceived,
        onDone: _onDisconnected,
        onError: (err) {
          debugPrint('[Bridge] Socket error: $err');
          _onDisconnected();
        },
      );
      isConnected.value = true;
      debugPrint('[Bridge] Connected to Python Core.');
    } catch (e) {
      debugPrint('[Bridge] Connection failed: $e');
      _onDisconnected();
    }
  }

  void _onMessageReceived(dynamic rawData) {
    try {
      final data = jsonDecode(rawData as String) as Map<String, dynamic>;
      final event = data['event'] as String?;
      
      if (event == 'STATE_SYNC') {
        gameState.value = data['data'] as Map<String, dynamic>;
      }
      
      _eventsController.add(data);
    } catch (e) {
      debugPrint('[Bridge] Error parsing payload: $e');
    }
  }

  void _onDisconnected() {
    isConnected.value = false;
    // Auto-reconnect after 2 seconds
    Future.delayed(const Duration(seconds: 2), () {
      if (!isConnected.value) {
        _connectWebSocket();
      }
    });
  }

  /// Send an action command to the Python backend.
  void sendAction(String type, [Map<String, dynamic>? payload]) {
    if (_channel != null && isConnected.value) {
      final message = jsonEncode({
        'type': type,
        'payload': payload ?? {},
      });
      _channel!.sink.add(message);
    } else {
      debugPrint('[Bridge] Cannot send action $type: Disconnected.');
    }
  }

  void dispose() {
    _subscription?.cancel();
    _channel?.sink.close();
    _pythonProcess?.kill();
    _eventsController.close();
    gameState.dispose();
    isConnected.dispose();
  }
}
