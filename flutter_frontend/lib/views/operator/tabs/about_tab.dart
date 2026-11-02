import 'package:flutter/material.dart';
import '../../../core/constants/game_colors.dart';

class AboutTab extends StatelessWidget {
  const AboutTab({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 28),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 960),
          child: Container(
            padding: const EdgeInsets.all(32),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: Colors.grey.shade400),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.04),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'About the Game Project',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.black87,
                  ),
                ),
                const SizedBox(height: 18),

                const Text(
                  'This game project is a custom-designed quiz game that captures the excitement and competitive spirit of classic family game shows. Inspired by formats like "Family Feud," it brings an engaging and interactive experience to any social gathering, party, or team-building event.\n\n'
                  'In the game, two teams, Team A and Team B, compete by guessing the most popular answers to a series of survey questions across multiple rounds. Each round presents a new question with top answers that carry specific point values. Teams take turns attempting to reveal all correct answers while avoiding strikes for incorrect guesses. Accumulating three strikes gives the opposing team a chance to steal the round by providing one of the remaining correct answers, adding a layer of strategy and excitement.',
                  style: TextStyle(fontSize: 13, height: 1.6, color: Colors.black87),
                ),
                const SizedBox(height: 20),

                const Text(
                  'The game features:',
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.black87),
                ),
                const SizedBox(height: 8),

                _buildFeatureBullet(
                  'Multiple Rounds with Increasing Stakes',
                  'Each round intensifies the competition with more challenging questions and higher point values (1x in Rounds 1 & 2, 2x Double in Round 3, and 3x Triple in Round 4).',
                ),
                _buildFeatureBullet(
                  'Steal Mechanism',
                  'Teams can seize opportunities to steal banked points from their opponents when three strikes occur, keeping the gameplay dynamic and unpredictable.',
                ),
                _buildFeatureBullet(
                  'Intuitive Control Panel',
                  'A user-friendly operator interface allows the game administrator to manage rounds smoothly, reveal answers, tally scores, handle steals, and ensure an enjoyable flow of the game.',
                ),
                _buildFeatureBullet(
                  'Engaging Visuals and Sound Effects',
                  'Animated 3D flip card graphics, strike pop-ins (X, XX, XXX), and authentic audio cues enhance the immersive experience for all participants.',
                ),
                _buildFeatureBullet(
                  'Dual-Display Architecture',
                  'Dedicated secondary display output allows clean projector broadcasting to the audience and contestants without showing operator controls.',
                ),
                const SizedBox(height: 16),

                const Text(
                  'Developed with flexibility in mind, the game can be customized to suit different audiences and occasions. It promotes teamwork, quick thinking, and friendly competition, making it an excellent choice for creating memorable moments among friends, family, or colleagues.\n\n'
                  'Please note that this game is a fan-made project created for educational and entertainment purposes. It is not affiliated with, endorsed by, or associated with any official game show or television program.',
                  style: TextStyle(fontSize: 13, height: 1.6, color: Colors.black87),
                ),
                const SizedBox(height: 28),

                const Divider(),
                const SizedBox(height: 20),

                // Comprehensive Game Rules & Operator Reference
                const Text(
                  'Game Rules & Mechanics Reference',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: GameColors.primaryBlue,
                  ),
                ),
                const SizedBox(height: 12),

                _buildSubSection('1. Face-Off & Podium Buzz-in'),
                _buildDetailText(
                  'At the beginning of each round, one representative from Team A and Team B approach the podium for the Face-Off question. The first contestant to buzz in provides an answer:\n'
                  '• If they give the #1 survey answer, their team immediately gains control of the board.\n'
                  '• If their answer is on the board but not #1, the opposing contestant may guess. Whichever team has the higher-ranked answer wins control (or may choose to pass to the opponents).',
                ),
                const SizedBox(height: 14),

                _buildSubSection('2. Playing the Board & Striking Out'),
                _buildDetailText(
                  'The controlling team works down the remaining unrevealed survey answers:\n'
                  '• Each correct guess reveals the answer card and banks points multiplied by the current round multiplier (1x, 2x, or 3x).\n'
                  '• An incorrect guess or failure to respond within the timer results in a Strike (X).\n'
                  '• If the team successfully reveals all answers before 3 strikes, they win the round and all banked points.',
                ),
                const SizedBox(height: 14),

                _buildSubSection('3. The Steal'),
                _buildDetailText(
                  'If the playing team accumulates three strikes (XXX), control immediately transfers to the opposing team. The opposing team briefly confers, and their designated captain gives one final answer:\n'
                  '• If the answer is on the board, the opposing team STEALS all accumulated points in the round bank.\n'
                  '• If the answer is incorrect, the original playing team keeps all their banked points.',
                ),
                const SizedBox(height: 14),

                _buildSubSection('4. Fast Money Finale'),
                _buildDetailText(
                  'The team with the highest point total after Round 4 advances to Fast Money:\n'
                  '• Two contestants from the winning team play. Player 1 has 20 seconds to answer 5 rapid survey questions.\n'
                  '• Player 2 is sequestered off-stage, then has 25 seconds to answer the same 5 questions (with a buzzer warning to provide an alternate answer if a duplicate is given).\n'
                  '• If their combined score reaches 200 points or more, the team wins the grand championship!',
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFeatureBullet(String title, String description) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('• ', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: GameColors.gameGreen)),
          Expanded(
            child: RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 13, height: 1.5, color: Colors.black87),
                children: [
                  TextSpan(text: '$title: ', style: const TextStyle(fontWeight: FontWeight.bold)),
                  TextSpan(text: description),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSubSection(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6.0),
      child: Text(
        title,
        style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: GameColors.gameGreen),
      ),
    );
  }

  Widget _buildDetailText(String text) {
    return Text(
      text,
      style: const TextStyle(fontSize: 12.5, height: 1.5, color: Colors.black87),
    );
  }
}
