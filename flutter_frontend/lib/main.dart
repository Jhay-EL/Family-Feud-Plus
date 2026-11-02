import 'package:flutter/material.dart';
import 'core/services/game_bridge.dart';
import 'core/theme/game_theme.dart';
import 'views/operator/operator_console_screen.dart';
import 'views/presentation/presentation_screen.dart';

void main(List<String> args) async {
  WidgetsFlutterBinding.ensureInitialized();

  final bridge = GameBridgeService();
  await bridge.initialize();

  // Check if launched as presentation display or operator console
  final isPresentationMode = args.contains('--presentation');

  runApp(FamilyFeudApp(
    bridge: bridge,
    isPresentationMode: isPresentationMode,
  ));
}

class FamilyFeudApp extends StatelessWidget {
  final GameBridgeService bridge;
  final bool isPresentationMode;

  const FamilyFeudApp({
    Key? key,
    required this.bridge,
    required this.isPresentationMode,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: isPresentationMode ? 'Family Feud+ Board' : 'Family Feud+ Console',
      debugShowCheckedModeBanner: false,
      theme: GameTheme.lightTheme,
      home: isPresentationMode
          ? PresentationScreen(bridge: bridge)
          : OperatorConsoleScreen(bridge: bridge),
    );
  }
}
