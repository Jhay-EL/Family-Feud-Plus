import 'package:flutter/material.dart';
import '../../core/constants/game_colors.dart';
import '../../core/services/game_bridge.dart';
import 'tabs/welcome_tab.dart';
import 'tabs/face_off_tab.dart';
import 'tabs/fast_money_tab.dart';
import 'tabs/about_tab.dart';

class OperatorConsoleScreen extends StatefulWidget {
  final GameBridgeService bridge;

  const OperatorConsoleScreen({Key? key, required this.bridge}) : super(key: key);

  @override
  State<OperatorConsoleScreen> createState() => _OperatorConsoleScreenState();
}

class _OperatorConsoleScreenState extends State<OperatorConsoleScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: widget.bridge,
      builder: (context, _) {
        final state = widget.bridge.state;
        final isConnected = widget.bridge.isConnected;

        return Scaffold(
          appBar: AppBar(
            backgroundColor: GameColors.surfaceLight,
            elevation: 0,
            titleSpacing: 16,
            title: Row(
              children: [
                const Text(
                  'Family Feud+ Console',
                  style: TextStyle(
                    color: GameColors.primaryBlue,
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
                const SizedBox(width: 16),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: isConnected ? GameColors.gameGreen.withOpacity(0.15) : GameColors.strikeRed.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isConnected ? GameColors.gameGreen : GameColors.strikeRed,
                    ),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        width: 8,
                        height: 8,
                        decoration: BoxDecoration(
                          color: isConnected ? GameColors.gameGreen : GameColors.strikeRed,
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 6),
                      Text(
                        isConnected ? 'Engine Connected' : 'Engine Offline',
                        style: TextStyle(
                          color: isConnected ? GameColors.gameGreen : GameColors.strikeRed,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            bottom: PreferredSize(
              preferredSize: const Size.fromHeight(42),
              child: Container(
                color: GameColors.borderLight.withOpacity(0.4),
                child: TabBar(
                  controller: _tabController,
                  tabs: const [
                    Tab(text: 'Welcome Screen'),
                    Tab(text: 'Face Off Round'),
                    Tab(text: 'Fast Money Round'),
                    Tab(text: 'About & Mechanics'),
                  ],
                ),
              ),
            ),
          ),
          body: TabBarView(
            controller: _tabController,
            children: [
              WelcomeTab(
                bridge: widget.bridge,
                onOpenFaceOff: () => _tabController.animateTo(1),
                onOpenFastMoney: () => _tabController.animateTo(2),
                onOpenAbout: () => _tabController.animateTo(3),
              ),
              FaceOffTab(
                bridge: widget.bridge,
                state: state,
              ),
              FastMoneyTab(
                bridge: widget.bridge,
                state: state,
              ),
              const AboutTab(),
            ],
          ),
        );
      },
    );
  }
}
