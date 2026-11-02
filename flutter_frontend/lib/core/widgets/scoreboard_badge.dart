import 'package:flutter/material.dart';
import '../constants/game_colors.dart';

class ScoreboardBadge extends StatelessWidget {
  final String label;
  final int points;
  final double fontSize;
  final Color backgroundColor;

  const ScoreboardBadge({
    Key? key,
    required this.label,
    required this.points,
    this.fontSize = 42,
    this.backgroundColor = Colors.black87,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: GameColors.goldAmber, width: 3),
        boxShadow: const [
          BoxShadow(color: Colors.black45, blurRadius: 6, offset: Offset(0, 4)),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (label.isNotEmpty)
            Text(
              label.toUpperCase(),
              style: const TextStyle(
                color: GameColors.goldAmber,
                fontSize: 12,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.2,
              ),
            ),
          Text(
            '$points',
            style: TextStyle(
              fontFamily: 'Consolas',
              fontSize: fontSize,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
