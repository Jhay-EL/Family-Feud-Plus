import 'package:flutter/material.dart';
import '../../core/services/game_bridge.dart';

class TitleScreenView extends StatefulWidget {
  final GameBridgeService bridge;

  const TitleScreenView({Key? key, required this.bridge}) : super(key: key);

  @override
  State<TitleScreenView> createState() => _TitleScreenViewState();
}

class _TitleScreenViewState extends State<TitleScreenView>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2200),
    )..repeat(reverse: true);

    _scaleAnimation = Tween<double>(begin: 0.96, end: 1.04).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        // Background Image
        Image.asset(
          'res/bg/Welcome Screen BG.png',
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => Container(
            decoration: const BoxDecoration(
              gradient: RadialGradient(
                center: Alignment.center,
                radius: 0.9,
                colors: [Color(0xFF5BA4E6), Color(0xFF1E528E)],
              ),
            ),
          ),
        ),

        // Glowing Animated Centered Logo
        Center(
          child: ScaleTransition(
            scale: _scaleAnimation,
            child: Container(
              decoration: BoxDecoration(
                boxShadow: [
                  BoxShadow(
                    color: Colors.white.withOpacity(0.35),
                    blurRadius: 40,
                    spreadRadius: 10,
                  ),
                ],
              ),
              child: Image.asset(
                'res/mipmap/Family-Feud-Logo.png',
                width: 720,
                fit: BoxFit.contain,
                errorBuilder: (_, __, ___) => const Text(
                  'FAMILY FEUD',
                  style: TextStyle(
                    fontSize: 72,
                    fontWeight: FontWeight.bold,
                    color: Colors.amber,
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
