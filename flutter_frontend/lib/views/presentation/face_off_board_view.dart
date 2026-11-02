import 'package:flutter/material.dart';
import '../../core/models/game_models.dart';
import '../../core/services/game_bridge.dart';
import '../../core/widgets/answer_flip_card.dart';
import '../../core/widgets/strike_overlay.dart';
import '../../core/widgets/scoreboard_badge.dart';

class FaceOffBoardView extends StatefulWidget {
  final GameBridgeService bridge;
  final GameStateModel state;

  const FaceOffBoardView({
    Key? key,
    required this.bridge,
    required this.state,
  }) : super(key: key);

  @override
  State<FaceOffBoardView> createState() => _FaceOffBoardViewState();
}

class _FaceOffBoardViewState extends State<FaceOffBoardView> {
  int _activeStrikeOverlay = 0;

  @override
  Widget build(BuildContext context) {
    final state = widget.state;
    final q = state.activeQuestion;
    final answers = q?.answers ?? [];

    if (state.currentStrikeDisplay > 0 && _activeStrikeOverlay == 0) {
      _activeStrikeOverlay = state.currentStrikeDisplay;
    }

    return Stack(
      fit: StackFit.expand,
      children: [
        // Background Image Canvas
        Image.asset(
          'res/img/Main Game.png',
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => Container(
            decoration: const BoxDecoration(
              gradient: RadialGradient(
                center: Alignment.center,
                radius: 1.0,
                colors: [Color(0xFF003080), Color(0xFF001133)],
              ),
            ),
          ),
        ),

        // 16:9 Responsive Broadcast Board
        Center(
          child: AspectRatio(
            aspectRatio: 16 / 9,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 24),
              child: Column(
                children: [
                  // Top Header: Team A, Bank Score, Team B
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      // Team A
                      ScoreboardBadge(
                        label: state.teamA.name.isNotEmpty ? state.teamA.name : 'Team A',
                        points: state.teamA.totalPoints,
                        fontSize: 44,
                      ),

                      // Center Pot / Bank
                      ScoreboardBadge(
                        label: 'Round Bank (${state.multiplier}x)',
                        points: state.bankPoints,
                        fontSize: 50,
                        backgroundColor: const Color(0xFF002255),
                      ),

                      // Team B
                      ScoreboardBadge(
                        label: state.teamB.name.isNotEmpty ? state.teamB.name : 'Team B',
                        points: state.teamB.totalPoints,
                        fontSize: 44,
                      ),
                    ],
                  ),
                  const SizedBox(height: 32),

                  // Main 8-Answer Board (2 Columns of 4 Flip Cards)
                  Expanded(
                    child: Row(
                      children: [
                        // Left Column (Answers 1 to 4)
                        Expanded(
                          child: Column(
                            children: [
                              for (int i = 1; i <= 4; i++)
                                Expanded(
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(vertical: 5.0),
                                    child: _buildAnswerSlot(i, answers),
                                  ),
                                ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 32),

                        // Right Column (Answers 5 to 8)
                        Expanded(
                          child: Column(
                            children: [
                              for (int i = 5; i <= 8; i++)
                                Expanded(
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(vertical: 5.0),
                                    child: _buildAnswerSlot(i, answers),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),

        // Strike Overlay Pop-in
        if (_activeStrikeOverlay > 0)
          StrikeOverlay(
            strikeCount: _activeStrikeOverlay,
            onDismissed: () {
              setState(() {
                _activeStrikeOverlay = 0;
              });
              widget.bridge.sendAction('CLEAR_STRIKE_DISPLAY');
            },
          ),
      ],
    );
  }

  Widget _buildAnswerSlot(int index, List<AnswerModel> answers) {
    final ans = answers.firstWhere(
      (a) => a.index == index,
      orElse: () => AnswerModel(id: 0, index: index, text: '', points: 0, isRevealed: false),
    );

    if (ans.text.isEmpty) {
      // Empty / hidden slot
      return Opacity(
        opacity: 0.15,
        child: Container(
          decoration: BoxDecoration(
            color: Colors.black45,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.white24, width: 2),
          ),
        ),
      );
    }

    return AnswerFlipCard(
      index: index,
      answerText: ans.text,
      points: ans.points,
      isRevealed: ans.isRevealed,
    );
  }
}
