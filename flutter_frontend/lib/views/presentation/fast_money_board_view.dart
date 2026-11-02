import 'package:flutter/material.dart';
import '../../core/constants/game_colors.dart';
import '../../core/models/game_models.dart';
import '../../core/services/game_bridge.dart';

class FastMoneyBoardView extends StatelessWidget {
  final GameBridgeService bridge;
  final GameStateModel state;

  const FastMoneyBoardView({
    Key? key,
    required this.bridge,
    required this.state,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final fm = state.fastMoney;
    final isWinning = fm.totalPoints >= 200;

    return Stack(
      fit: StackFit.expand,
      children: [
        // Background Image Canvas
        Image.asset(
          'res/bg/Fast Money Round.png',
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => Container(
            color: const Color(0xFF001A40),
          ),
        ),

        // Responsive AspectRatio Canvas
        Center(
          child: AspectRatio(
            aspectRatio: 16 / 9,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 24),
              child: Column(
                children: [
                  // Top Timer Display
                  Container(
                    width: 180,
                    height: 70,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.4),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.white30, width: 2),
                    ),
                    child: Text(
                      fm.timer > 0 ? '${fm.timer}' : '00',
                      style: const TextStyle(
                        fontFamily: 'Consolas',
                        fontSize: 48,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Two Columns: Player 1 & Player 2
                  Expanded(
                    child: Row(
                      children: [
                        // Player 1 Column
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              for (int i = 0; i < 5; i++)
                                _buildFastMoneyRow(
                                  i < fm.p1Entries.length ? fm.p1Entries[i] : null,
                                ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 48),

                        // Player 2 Column
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              for (int i = 0; i < 5; i++)
                                _buildFastMoneyRow(
                                  i < fm.p2Entries.length ? fm.p2Entries[i] : null,
                                ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Bottom Total Score Bar
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 8),
                        decoration: BoxDecoration(
                          color: isWinning ? GameColors.gameGreen : Colors.black.withOpacity(0.6),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(
                            color: isWinning ? Colors.white : GameColors.goldAmber,
                            width: 2,
                          ),
                          boxShadow: isWinning
                              ? [
                                  BoxShadow(
                                    color: GameColors.gameGreen.withOpacity(0.8),
                                    blurRadius: 20,
                                    spreadRadius: 4,
                                  ),
                                ]
                              : [],
                        ),
                        child: Text(
                          'TOTAL: ${fm.totalPoints}',
                          style: TextStyle(
                            fontFamily: 'Consolas',
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: isWinning ? Colors.white : GameColors.goldAmber,
                          ),
                        ),
                      ),
                      const SizedBox(width: 20),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),

        // Grand Prize Winner Banner
        if (isWinning)
          Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 24),
              decoration: BoxDecoration(
                color: GameColors.gameGreen.withOpacity(0.95),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.white, width: 4),
                boxShadow: const [
                  BoxShadow(color: Colors.black54, blurRadius: 30, spreadRadius: 10),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: const [
                  Text(
                    'WINNER! 200+ POINTS!',
                    style: TextStyle(
                      fontFamily: 'Consolas',
                      fontSize: 44,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      letterSpacing: 2,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'CONGRATULATIONS!',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: GameColors.goldAmber,
                    ),
                  ),
                ],
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildFastMoneyRow(FastMoneyEntryModel? entry) {
    final text = entry?.isRevealed == true ? entry!.answer : '';
    final points = entry?.isPointsRevealed == true ? '${entry!.points}' : '';

    return Container(
      height: 64,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: const Color(0xFF002A66),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: const Color(0xFF1E528E), width: 2),
      ),
      child: Row(
        children: [
          // Answer text
          Expanded(
            child: Text(
              text.toUpperCase(),
              style: const TextStyle(
                fontFamily: 'Consolas',
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                letterSpacing: 1.2,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
          // Points box
          Container(
            width: 60,
            alignment: Alignment.center,
            decoration: const BoxDecoration(
              border: Border(left: BorderSide(color: Color(0xFF1E528E), width: 2)),
            ),
            child: Text(
              points,
              style: const TextStyle(
                fontFamily: 'Consolas',
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: GameColors.goldAmber,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
