import 'dart:math';
import 'package:flutter/material.dart';
import '../constants/game_colors.dart';

class AnswerFlipCard extends StatefulWidget {
  final int index;
  final String answerText;
  final int points;
  final bool isRevealed;
  final VoidCallback? onTap;

  const AnswerFlipCard({
    Key? key,
    required this.index,
    required this.answerText,
    required this.points,
    required this.isRevealed,
    this.onTap,
  }) : super(key: key);

  @override
  State<AnswerFlipCard> createState() => _AnswerFlipCardState();
}

class _AnswerFlipCardState extends State<AnswerFlipCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
    _animation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutBack),
    );

    if (widget.isRevealed) {
      _controller.value = 1.0;
    }
  }

  @override
  void didUpdateWidget(AnswerFlipCard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isRevealed != oldWidget.isRevealed) {
      if (widget.isRevealed) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onTap,
      child: AnimatedBuilder(
        animation: _animation,
        builder: (context, child) {
          final angle = _animation.value * pi;
          final isUnder = angle > pi / 2;

          return Transform(
            alignment: Alignment.center,
            transform: Matrix4.identity()
              ..setEntry(3, 2, 0.001)
              ..rotateX(angle),
            child: isUnder ? _buildRevealedFace() : _buildHiddenFace(),
          );
        },
      ),
    );
  }

  Widget _buildHiddenFace() {
    return Container(
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [GameColors.primaryBlue, GameColors.primaryBlueDark],
        ),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: GameColors.goldAmber, width: 2.5),
        boxShadow: const [
          BoxShadow(color: Colors.black38, blurRadius: 4, offset: Offset(0, 3)),
        ],
      ),
      child: Center(
        child: Container(
          width: 46,
          height: 46,
          decoration: BoxDecoration(
            color: Colors.white,
            shape: BoxShape.circle,
            border: Border.all(color: GameColors.goldAmber, width: 3),
            boxShadow: const [
              BoxShadow(color: Colors.black26, blurRadius: 3),
            ],
          ),
          child: Center(
            child: Text(
              '${widget.index}',
              style: const TextStyle(
                fontFamily: 'Arial',
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: GameColors.primaryBlue,
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRevealedFace() {
    return Transform(
      alignment: Alignment.center,
      transform: Matrix4.identity()..rotateX(pi),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: GameColors.primaryBlue, width: 2.5),
          boxShadow: const [
            BoxShadow(color: Colors.black38, blurRadius: 4, offset: Offset(0, 3)),
          ],
        ),
        padding: const EdgeInsets.symmetric(horizontal: 14),
        child: Row(
          children: [
            Expanded(
              child: Text(
                widget.answerText.toUpperCase(),
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: GameColors.primaryBlue,
                  letterSpacing: 0.5,
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              decoration: BoxDecoration(
                color: GameColors.primaryBlue,
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                '${widget.points}',
                style: const TextStyle(
                  fontFamily: 'Consolas',
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
