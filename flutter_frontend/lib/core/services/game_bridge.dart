import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/game_models.dart';

class GameBridgeService extends ChangeNotifier {
  static const String defaultUrl = 'ws://127.0.0.1:8765/ws';

  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  Process? _pythonProcess;

  GameStateModel? _state;
  List<Map<String, dynamic>> _questionsList = [];
  bool _isConnected = false;
  String _statusMessage = 'Disconnected';

  GameStateModel? get state => _state;
  List<Map<String, dynamic>> get questionsList => _questionsList;
  bool get isConnected => _isConnected;
  String get statusMessage => _statusMessage;

  Future<void> initialize() async {
    await _ensureBackendRunning();
    await connect();
    requestQuestionsList();
  }

  Future<void> _ensureBackendRunning() async {
    try {
      final socket = await Socket.connect('127.0.0.1', 8765,
          timeout: const Duration(milliseconds: 500));
      await socket.close();
      debugPrint('[Bridge] Python backend already active on 8765.');
    } catch (_) {
      debugPrint('[Bridge] Spawning Python backend process...');
      try {
        _pythonProcess = await Process.start(
          'python3',
          ['backend/server.py'],
          mode: ProcessStartMode.detached,
        );
        await Future.delayed(const Duration(seconds: 1));
      } catch (e) {
        debugPrint('[Bridge] Could not auto-spawn Python backend: $e');
      }
    }
  }

  Future<void> connect([String url = defaultUrl]) async {
    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));
      _subscription = _channel!.stream.listen(
        _onMessageReceived,
        onDone: _onDisconnected,
        onError: (err) {
          debugPrint('[Bridge] Error: $err');
          _onDisconnected();
        },
      );
      _isConnected = true;
      _statusMessage = 'Connected to Family Feud Core';
      notifyListeners();
    } catch (e) {
      debugPrint('[Bridge] Connection error: $e');
      _onDisconnected();
    }
  }

  void _onMessageReceived(dynamic rawData) {
    try {
      final json = jsonDecode(rawData as String) as Map<String, dynamic>;
      final event = json['event'] as String?;

      if (event == 'STATE_SYNC') {
        final data = json['data'] as Map<String, dynamic>? ?? {};
        _state = GameStateModel.fromJson(data);
        notifyListeners();
      } else if (event == 'QUESTIONS_LIST') {
        final rawList = json['data'] as List<dynamic>? ?? [];
        _questionsList = rawList.map((e) => e as Map<String, dynamic>).toList();
        notifyListeners();
      }
    } catch (e) {
      debugPrint('[Bridge] Parse error: $e');
    }
  }

  void _onDisconnected() {
    _isConnected = false;
    _statusMessage = 'Disconnected from Core (Retrying...)';
    notifyListeners();

    // Auto reconnect loop
    Future.delayed(const Duration(seconds: 2), () {
      if (!_isConnected) {
        connect();
      }
    });
  }

  void sendAction(String type, [Map<String, dynamic>? payload]) {
    if (_channel != null && _isConnected) {
      final msg = jsonEncode({
        'type': type,
        'payload': payload ?? {},
      });
      _channel!.sink.add(msg);
    }
  }

  // Convenience Action methods
  void setActiveScreen(String screen) => sendAction('SET_ACTIVE_SCREEN', {'screen': screen});
  void revealAnswer(int index) => sendAction('REVEAL_ANSWER', {'index': index});
  void addStrike(String team) => sendAction('ADD_STRIKE', {'team': team});
  void rewardPoints(String team) => sendAction('REWARD_POINTS', {'team': team});
  void setMultiplier(int mult) => sendAction('SET_MULTIPLIER', {'multiplier': mult});
  void logRound() => sendAction('LOG_ROUND');
  void loadQuestion(int id) => sendAction('LOAD_QUESTION', {'id': id});
  void setTeamNames(String teamA, String teamB) =>
      sendAction('SET_TEAM_NAMES', {'team_a': teamA, 'team_b': teamB});
  void playAudio(String cue) => sendAction('PLAY_AUDIO', {'cue': cue});
  void setFastMoneyEntry(int player, int index, String answer, int points) =>
      sendAction('FM_SET_ENTRY', {'player': player, 'index': index, 'answer': answer, 'points': points});
  void revealFastMoneyAnswer(int player, int index) =>
      sendAction('FM_REVEAL_ANSWER', {'player': player, 'index': index});
  void revealFastMoneyPoints(int player, int index) =>
      sendAction('FM_REVEAL_POINTS', {'player': player, 'index': index});
  void resetFastMoney() => sendAction('FM_RESET');
  void requestQuestionsList([String roundType = 'face_off']) =>
      sendAction('GET_QUESTIONS_LIST', {'round_type': roundType});
  void saveQuestion(String question, List<List<dynamic>> answers, [int? id]) =>
      sendAction('SAVE_QUESTION', {'question': question, 'answers': answers, 'id': id});
  void deleteQuestion(int id) => sendAction('DELETE_QUESTION', {'id': id});

  @override
  void dispose() {
    _subscription?.cancel();
    _channel?.sink.close();
    _pythonProcess?.kill();
    super.dispose();
  }
}
