import 'package:flutter/material.dart';

/// Overlay widget rendering animated Strike X, XX, or XXX marks.
class StrikeOverlay extends StatefulWidget {
  final int strikeCount; // 1, 2, or 3
  final VoidCallback onDismissed;

  const StrikeOverlay({
    Key? key,
    required this.strikeCount,
    required this.onDismissed,
  }) : super(key: key);

  @override
  State<StrikeOverlay> createState() => _StrikeOverlayState();
}

class _StrikeOverlayState extends State<StrikeOverlay>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _opacityAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1800),
    );

    _scaleAnimation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 0.2, end: 1.15), weight: 20),
      TweenSequenceItem(tween: Tween(begin: 1.15, end: 1.0), weight: 10),
      TweenSequenceItem(tween: ConstantTween(1.0), weight: 50),
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.3), weight: 20),
    ]).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));

    _opacityAnimation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 0.0, end: 1.0), weight: 15),
      TweenSequenceItem(tween: ConstantTween(1.0), weight: 65),
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 0.0), weight: 20),
    ]).animate(_controller);

    _controller.forward().then((_) => widget.onDismissed());
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  String get _strikeAssetPath {
    switch (widget.strikeCount) {
      case 2:
        return 'res/mipmap/XX.png';
      case 3:
        return 'res/mipmap/XXX.png';
      case 1:
      default:
        return 'res/mipmap/X.png';
    }
  }

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Opacity(
            opacity: _opacityAnimation.value,
            child: Transform.scale(
              scale: _scaleAnimation.value,
              child: Center(
                child: Image.asset(
                  _strikeAssetPath,
                  height: 380,
                  fit: BoxFit.contain,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
