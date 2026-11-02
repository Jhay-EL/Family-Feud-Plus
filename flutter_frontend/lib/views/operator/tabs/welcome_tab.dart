import 'dart:io';
import 'package:flutter/material.dart';
import '../../../core/constants/game_colors.dart';
import '../../../core/services/game_bridge.dart';

class WelcomeTab extends StatefulWidget {
  final GameBridgeService bridge;
  final VoidCallback onOpenFaceOff;
  final VoidCallback onOpenFastMoney;
  final VoidCallback onOpenAbout;

  const WelcomeTab({
    Key? key,
    required this.bridge,
    required this.onOpenFaceOff,
    required this.onOpenFastMoney,
    required this.onOpenAbout,
  }) : super(key: key);

  @override
  State<WelcomeTab> createState() => _WelcomeTabState();
}

class _WelcomeTabState extends State<WelcomeTab> {
  String _selectedMonitor = 'Monitor 2:';

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        // Left Column: Control Buttons & Display Picker (Flex 4)
        Expanded(
          flex: 4,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 40.0, vertical: 36.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Family Feud+',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: GameColors.primaryBlue,
                    letterSpacing: 0.5,
                  ),
                ),
                const SizedBox(height: 6),
                const Text(
                  'Guessing the most popular answers to survey questions',
                  style: TextStyle(
                    fontSize: 14,
                    color: GameColors.primaryBlue,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 36),

                // Navigation Buttons (Matching Screenshot 1)
                _buildActionButton(
                  label: 'Title Screen',
                  onPressed: () {
                    widget.bridge.setActiveScreen('title');
                    widget.bridge.playAudio('intro');
                  },
                ),
                const SizedBox(height: 12),

                _buildActionButton(
                  label: 'Face Off Round',
                  onPressed: () {
                    widget.bridge.setActiveScreen('face_off');
                    widget.onOpenFaceOff();
                  },
                ),
                const SizedBox(height: 12),

                _buildActionButton(
                  label: 'Fast Money Round',
                  onPressed: () {
                    widget.bridge.setActiveScreen('fast_money');
                    widget.onOpenFastMoney();
                  },
                ),
                const SizedBox(height: 12),

                _buildActionButton(
                  label: 'Game Mechanics',
                  onPressed: widget.onOpenAbout,
                ),

                const Spacer(),

                // Display Selection
                const Text(
                  'Select the display to deploy the game screen',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: GameColors.primaryBlue,
                  ),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14),
                  decoration: BoxDecoration(
                    color: const Color(0xFFD8D8D8),
                    borderRadius: BorderRadius.circular(4),
                    border: Border.all(color: Colors.grey.shade400),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      isExpanded: true,
                      value: _selectedMonitor,
                      icon: const Icon(Icons.arrow_drop_down, color: GameColors.primaryBlue),
                      style: const TextStyle(
                        color: GameColors.primaryBlue,
                        fontWeight: FontWeight.bold,
                        fontSize: 13,
                      ),
                      items: const [
                        DropdownMenuItem(
                          value: 'Monitor 1: Primary',
                          child: Text('Monitor 1: Primary'),
                        ),
                        DropdownMenuItem(
                          value: 'Monitor 2:',
                          child: Text('Monitor 2: Secondary / Projector'),
                        ),
                      ],
                      onChanged: (val) {
                        if (val != null) {
                          setState(() {
                            _selectedMonitor = val;
                          });
                        }
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 28),

                // Quit Button
                ElevatedButton(
                  onPressed: () => _confirmQuit(context),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: GameColors.strikeRed,
                    minimumSize: const Size.fromHeight(42),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
                  ),
                  child: const Text(
                    'Quit',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),

        // Right Column: Scaled Hero Image & Background (Flex 6)
        Expanded(
          flex: 6,
          child: Stack(
            fit: StackFit.expand,
            children: [
              Image.asset(
                'res/bg/Welcome Screen BG.png',
                fit: BoxFit.cover,
                errorBuilder: (_, __, ___) => Container(
                  decoration: const BoxDecoration(
                    gradient: RadialGradient(
                      center: Alignment.center,
                      radius: 0.9,
                      colors: [Color(0xFF8AC1EF), Color(0xFF387CB8)],
                    ),
                  ),
                ),
              ),
              Center(
                child: Image.asset(
                  'res/mipmap/Family-Feud-Logo.png',
                  width: 520,
                  fit: BoxFit.contain,
                  errorBuilder: (_, __, ___) => const Text(
                    'FAMILY FEUD',
                    style: TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildActionButton({required String label, required VoidCallback onPressed}) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: GameColors.gameGreen,
        minimumSize: const Size.fromHeight(42),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
      ),
      child: Text(
        label,
        style: const TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }

  void _confirmQuit(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Quit Family Feud+'),
        content: const Text('Are you sure you want to close the game session?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              exit(0);
            },
            style: ElevatedButton.styleFrom(backgroundColor: GameColors.strikeRed),
            child: const Text('Quit Game', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}
