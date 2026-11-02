import 'package:flutter/material.dart';
import '../../core/services/game_bridge.dart';
import 'title_screen_view.dart';
import 'face_off_board_view.dart';
import 'fast_money_board_view.dart';

class PresentationScreen extends StatelessWidget {
  final GameBridgeService bridge;

  const PresentationScreen({Key? key, required this.bridge}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: bridge,
      builder: (context, _) {
        final state = bridge.state;
        final screen = state?.activeScreen ?? 'welcome';

        Widget body;
        if (screen == 'title' || screen == 'welcome') {
          body = TitleScreenView(bridge: bridge);
        } else if (screen == 'fast_money') {
          body = state != null
              ? FastMoneyBoardView(bridge: bridge, state: state)
              : const Center(child: CircularProgressIndicator());
        } else {
          // Default to face_off board
          body = state != null
              ? FaceOffBoardView(bridge: bridge, state: state)
              : const Center(child: CircularProgressIndicator());
        }

        return Scaffold(
          backgroundColor: Colors.black,
          body: body,
        );
      },
    );
  }
}
