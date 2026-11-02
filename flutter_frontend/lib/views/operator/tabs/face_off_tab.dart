import 'dart:async';
import 'package:flutter/material.dart';
import '../../../core/constants/game_colors.dart';
import '../../../core/models/game_models.dart';
import '../../../core/services/game_bridge.dart';

class FaceOffTab extends StatefulWidget {
  final GameBridgeService bridge;
  final GameStateModel? state;

  const FaceOffTab({
    Key? key,
    required this.bridge,
    required this.state,
  }) : super(key: key);

  @override
  State<FaceOffTab> createState() => _FaceOffTabState();
}

class _FaceOffTabState extends State<FaceOffTab> {
  final TextEditingController _teamAController = TextEditingController();
  final TextEditingController _teamBController = TextEditingController();
  final TextEditingController _timerController = TextEditingController(text: '3');

  int _remainingTimer = 0;
  Timer? _countdownTimer;

  @override
  void initState() {
    super.initState();
    _updateControllersFromState();
  }

  @override
  void didUpdateWidget(covariant FaceOffTab oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.state != widget.state) {
      _updateControllersFromState();
    }
  }

  void _updateControllersFromState() {
    if (widget.state != null) {
      if (_teamAController.text != widget.state!.teamA.name) {
        _teamAController.text = widget.state!.teamA.name;
      }
      if (_teamBController.text != widget.state!.teamB.name) {
        _teamBController.text = widget.state!.teamB.name;
      }
    }
  }

  void _onTeamNamesChanged() {
    widget.bridge.setTeamNames(_teamAController.text, _teamBController.text);
  }

  void _startTimer() {
    _countdownTimer?.cancel();
    final sec = int.tryParse(_timerController.text) ?? 3;
    setState(() {
      _remainingTimer = sec;
    });

    _countdownTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_remainingTimer > 1) {
        setState(() {
          _remainingTimer--;
        });
      } else {
        timer.cancel();
        setState(() {
          _remainingTimer = 0;
        });
        widget.bridge.playAudio('strike');
      }
    });
  }

  @override
  void dispose() {
    _countdownTimer?.cancel();
    _teamAController.dispose();
    _teamBController.dispose();
    _timerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.state == null) {
      return const Center(child: CircularProgressIndicator());
    }

    final state = widget.state!;
    final q = state.activeQuestion;
    final answers = q?.answers ?? [];

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ================= COLUMN 1: TEAMS, SCORECARD & AUDIO =================
          Expanded(
            flex: 34,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Enter the names of the teams playing:',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Team Name Text Fields
                  Row(
                    children: [
                      Expanded(
                        child: _buildInputField(
                          controller: _teamAController,
                          hint: 'Team A',
                          onChanged: (_) => _onTeamNamesChanged(),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _buildInputField(
                          controller: _teamBController,
                          hint: 'Team B',
                          onChanged: (_) => _onTeamNamesChanged(),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),

                  // Team A and Team B Control Columns
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Team A Column
                      Expanded(
                        child: Column(
                          children: [
                            _buildInfoRow('Team A Points:', '${state.teamA.totalPoints}'),
                            const SizedBox(height: 8),
                            _buildInfoRow('Strikes:', '${state.teamA.strikes}'),
                            const SizedBox(height: 12),
                            _buildSmallButton(
                              label: 'Reward / Steal Points',
                              color: GameColors.gameGreen,
                              onPressed: () => widget.bridge.rewardPoints('A'),
                            ),
                            const SizedBox(height: 8),
                            _buildSmallButton(
                              label: 'Strike',
                              color: GameColors.strikeRed,
                              onPressed: () => widget.bridge.addStrike('A'),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 12),
                      // Team B Column
                      Expanded(
                        child: Column(
                          children: [
                            _buildInfoRow('Team B Points:', '${state.teamB.totalPoints}'),
                            const SizedBox(height: 8),
                            _buildInfoRow('Strikes:', '${state.teamB.strikes}'),
                            const SizedBox(height: 12),
                            _buildSmallButton(
                              label: 'Reward / Steal Points',
                              color: GameColors.gameGreen,
                              onPressed: () => widget.bridge.rewardPoints('B'),
                            ),
                            const SizedBox(height: 8),
                            _buildSmallButton(
                              label: 'Strike',
                              color: GameColors.strikeRed,
                              onPressed: () => widget.bridge.addStrike('B'),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Scorecard Table (R1 - R4)
                  _buildScorecardTable(state),
                  const SizedBox(height: 24),

                  // Game Audio Control Header
                  const Text(
                    'Game Audio Control',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Audio Buttons Row 1
                  Row(
                    children: [
                      Expanded(
                        child: _buildAudioButton('Intro Music', () => widget.bridge.playAudio('intro')),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildAudioButton('Face-off x1', () => widget.bridge.playAudio('face_off')),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildAudioButton('Winning Sound', () => widget.bridge.playAudio('win_sound')),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),

                  // Audio Buttons Row 2
                  Row(
                    children: [
                      Expanded(
                        child: _buildAudioButton('Outro Music', () => widget.bridge.playAudio('outro')),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildAudioButton('Correct Ans.', () => widget.bridge.playAudio('good_answer')),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildAudioButton(
                          'Strike/Timer',
                          () => widget.bridge.playAudio('strike'),
                          color: GameColors.strikeRed,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 16),

          // ================= COLUMN 2: QUESTION & 8 ANSWERS =================
          Expanded(
            flex: 38,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Game Questions View',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Question View Box
                  Container(
                    width: double.infinity,
                    height: 110,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFFC0C0C0),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: Colors.grey.shade500),
                    ),
                    alignment: Alignment.centerLeft,
                    child: Text(
                      q?.text.isNotEmpty == true ? q!.text : 'Select a question from the list to display',
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // 8 Answers List (Vertical Buttons with Points Box)
                  for (int i = 1; i <= 8; i++)
                    _buildAnswerControlRow(i, answers),

                  const SizedBox(height: 8),

                  // Total Points Display
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      const Text(
                        'Total Points:',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: GameColors.primaryBlue,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Container(
                        width: 80,
                        height: 34,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: const Color(0xFFC0C0C0),
                          borderRadius: BorderRadius.circular(4),
                          border: Border.all(color: Colors.grey.shade500),
                        ),
                        child: Text(
                          '${state.bankPoints}',
                          style: const TextStyle(
                            fontFamily: 'Consolas',
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Show answers count on Face-off window
                  const Text(
                    'Show answers count on Face-off window',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Show Answers Count',
                          color: GameColors.gameGreen,
                          onPressed: () => widget.bridge.sendAction('SHOW_ANSWERS_COUNT'),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Clear answer count',
                          color: GameColors.strikeRed,
                          onPressed: () => widget.bridge.sendAction('CLEAR_ANSWERS_COUNT'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 16),

          // ================= COLUMN 3: QUESTIONS LIST, EDIT, MULTIPLIERS =================
          Expanded(
            flex: 28,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Questions List
                  Container(
                    height: 150,
                    decoration: BoxDecoration(
                      color: const Color(0xFFC0C0C0),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: Colors.grey.shade500),
                    ),
                    child: ListView.builder(
                      itemCount: widget.bridge.questionsList.length,
                      itemBuilder: (context, idx) {
                        final item = widget.bridge.questionsList[idx];
                        final id = item['id'] as int;
                        final text = item['text'] as String;
                        final isSelected = widget.state?.activeQuestion?.id == id;

                        return Container(
                          color: isSelected ? const Color(0xFF606060) : Colors.transparent,
                          child: ListTile(
                            dense: true,
                            contentPadding: const EdgeInsets.symmetric(horizontal: 10),
                            title: Text(
                              'Question ${idx + 1}: $text',
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                                color: isSelected ? Colors.white : Colors.black87,
                              ),
                            ),
                            onTap: () {
                              widget.bridge.loadQuestion(id);
                            },
                          ),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 14),

                  // Add questions group
                  const Text(
                    'Add questions to the database',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 6),
                  _buildSmallButton(
                    label: 'Load from file (.csv only supported)',
                    color: GameColors.gameGreen,
                    onPressed: () => _showCsvImportDialog(context),
                  ),
                  const SizedBox(height: 6),
                  _buildSmallButton(
                    label: 'Manual add questions',
                    color: GameColors.cautionOrange,
                    onPressed: () => _showManualAddDialog(context),
                  ),
                  const SizedBox(height: 14),

                  // Edit questions and answers group
                  const Text(
                    'Edit questions and answers from the database',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Modify',
                          color: GameColors.cautionOrange,
                          onPressed: () => _showModifyDialog(context),
                        ),
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Save',
                          color: GameColors.gameGreen,
                          onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Question saved successfully.')),
                          ),
                        ),
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Delete',
                          color: GameColors.strikeRed,
                          onPressed: () {
                            if (widget.state?.activeQuestion != null) {
                              widget.bridge.deleteQuestion(widget.state!.activeQuestion!.id);
                            }
                          },
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),

                  // Round multiplier and timer
                  const Text(
                    'Round multiplier and timer',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: _buildSmallButton(
                          label: 'x2 Round',
                          color: widget.state?.multiplier == 2 ? GameColors.cautionOrange : GameColors.gameGreen,
                          onPressed: () => widget.bridge.setMultiplier(2),
                        ),
                      ),
                      const SizedBox(width: 10),
                      SizedBox(
                        width: 55,
                        height: 32,
                        child: TextField(
                          controller: _timerController,
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                          decoration: InputDecoration(
                            contentPadding: EdgeInsets.zero,
                            filled: true,
                            fillColor: const Color(0xFFE8E8E8),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(4)),
                          ),
                        ),
                      ),
                      const SizedBox(width: 6),
                      const Text('sec', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: _buildSmallButton(
                          label: 'x3 Round',
                          color: widget.state?.multiplier == 3 ? GameColors.strikeRed : GameColors.gameGreen,
                          onPressed: () => widget.bridge.setMultiplier(3),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _buildSmallButton(
                          label: _remainingTimer > 0 ? 'Timer: $_remainingTimer' : 'Start Timer',
                          color: _remainingTimer > 0 ? GameColors.cautionOrange : GameColors.gameGreen,
                          onPressed: _remainingTimer > 0 ? null : _startTimer,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Start over or clear the log
                  const Text(
                    'Start over or clear the log of the game',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: GameColors.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Log, Next round',
                          color: GameColors.gameGreen,
                          onPressed: () => widget.bridge.logRound(),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildSmallButton(
                          label: 'Reset All',
                          color: GameColors.strikeRed,
                          onPressed: () => widget.bridge.sendAction('RESET_MATCH'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // --- Subcomponents & Helpers ---

  Widget _buildInputField({
    required TextEditingController controller,
    required String hint,
    required ValueChanged<String> onChanged,
  }) {
    return Container(
      height: 38,
      decoration: BoxDecoration(
        color: const Color(0xFFE8E8E8),
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: Colors.grey.shade400),
      ),
      child: TextField(
        controller: controller,
        onChanged: onChanged,
        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
        decoration: InputDecoration(
          hintText: hint,
          contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
          border: InputBorder.none,
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
        ),
        Container(
          width: 70,
          height: 30,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: const Color(0xFFC0C0C0),
            borderRadius: BorderRadius.circular(4),
          ),
          child: Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, fontFamily: 'Consolas'),
          ),
        ),
      ],
    );
  }

  Widget _buildScorecardTable(GameStateModel state) {
    return Column(
      children: [
        Row(
          children: const [
            Expanded(child: Center(child: Text('Points', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)))),
            Expanded(child: Center(child: Text('Strikes', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)))),
            SizedBox(width: 12),
            Expanded(child: Center(child: Text('Points', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)))),
            Expanded(child: Center(child: Text('Strikes', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)))),
          ],
        ),
        const SizedBox(height: 4),
        for (int r = 1; r <= 4; r++)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 2.0),
            child: Row(
              children: [
                Text('R$r', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue)),
                const SizedBox(width: 4),
                Expanded(child: _buildScoreBox(_getRoundPoints(state, r, 'A'))),
                const SizedBox(width: 4),
                Expanded(child: _buildScoreBox(_getRoundStrikes(state, r, 'A'))),
                const SizedBox(width: 12),
                Text('R$r', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue)),
                const SizedBox(width: 4),
                Expanded(child: _buildScoreBox(_getRoundPoints(state, r, 'B'))),
                const SizedBox(width: 4),
                Expanded(child: _buildScoreBox(_getRoundStrikes(state, r, 'B'))),
              ],
            ),
          ),
      ],
    );
  }

  Widget _buildScoreBox(String text) {
    return Container(
      height: 28,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: const Color(0xFFC0C0C0),
        borderRadius: BorderRadius.circular(3),
      ),
      child: Text(
        text,
        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, fontFamily: 'Consolas'),
      ),
    );
  }

  String _getRoundPoints(GameStateModel state, int roundNum, String team) {
    final entry = state.matchLog.where((l) => l.roundNum == roundNum).firstOrNull;
    if (entry == null) return '';
    return team == 'A' ? '${entry.teamAPoints}' : '${entry.teamBPoints}';
  }

  String _getRoundStrikes(GameStateModel state, int roundNum, String team) {
    final entry = state.matchLog.where((l) => l.roundNum == roundNum).firstOrNull;
    if (entry == null) return '';
    return team == 'A' ? '${entry.teamAStrikes}' : '${entry.teamBStrikes}';
  }

  Widget _buildAnswerControlRow(int slotIndex, List<AnswerModel> answers) {
    final answer = answers.firstWhere(
      (a) => a.index == slotIndex,
      orElse: () => AnswerModel(id: 0, index: slotIndex, text: '', points: 0, isRevealed: false),
    );

    final hasData = answer.text.isNotEmpty;
    final isRevealed = answer.isRevealed;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        children: [
          // Green Answer Button
          Expanded(
            child: ElevatedButton(
              onPressed: hasData && !isRevealed ? () => widget.bridge.revealAnswer(slotIndex) : null,
              style: ElevatedButton.styleFrom(
                backgroundColor: isRevealed ? GameColors.primaryBlue : (hasData ? GameColors.gameGreen : const Color(0xFFC0C0C0)),
                foregroundColor: Colors.white,
                disabledBackgroundColor: isRevealed ? GameColors.primaryBlue : const Color(0xFFC0C0C0),
                disabledForegroundColor: isRevealed ? Colors.white : Colors.black54,
                minimumSize: const Size.fromHeight(34),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
              ),
              child: Text(
                hasData ? (isRevealed ? '$slotIndex. ${answer.text} (Revealed)' : '$slotIndex. ${answer.text}') : 'Answer $slotIndex',
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ),
          const SizedBox(width: 8),
          // Points Box
          Container(
            width: 60,
            height: 34,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: const Color(0xFFC0C0C0),
              borderRadius: BorderRadius.circular(3),
            ),
            child: Text(
              hasData ? '${answer.points}' : '',
              style: const TextStyle(fontFamily: 'Consolas', fontSize: 13, fontWeight: FontWeight.bold, color: Colors.black87),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSmallButton({
    required String label,
    required Color color,
    VoidCallback? onPressed,
  }) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        minimumSize: const Size.fromHeight(32),
        padding: const EdgeInsets.symmetric(horizontal: 8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
      ),
      child: Text(
        label,
        style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
        textAlign: TextAlign.center,
      ),
    );
  }

  Widget _buildAudioButton(String label, VoidCallback onPressed, {Color color = GameColors.gameGreen}) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        minimumSize: const Size.fromHeight(32),
        padding: EdgeInsets.zero,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
      ),
      child: Text(
        label,
        style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
        textAlign: TextAlign.center,
      ),
    );
  }

  void _showCsvImportDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Load Questions from CSV'),
        content: const Text(
          'Ensure your CSV file contains:\nQuestion, Answer 1, Pts 1, Answer 2, Pts 2...',
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(ctx).pop(), child: const Text('Close')),
        ],
      ),
    );
  }

  void _showManualAddDialog(BuildContext context) {
    final qController = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Manual Add Question'),
        content: TextField(
          controller: qController,
          decoration: const InputDecoration(labelText: 'Question Text'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(ctx).pop(), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () {
              if (qController.text.isNotEmpty) {
                widget.bridge.saveQuestion(qController.text, []);
                Navigator.of(ctx).pop();
              }
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showModifyDialog(BuildContext context) {
    final q = widget.state?.activeQuestion;
    if (q == null) return;
    final qController = TextEditingController(text: q.text);

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Modify Question'),
        content: TextField(
          controller: qController,
          decoration: const InputDecoration(labelText: 'Question Text'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(ctx).pop(), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () {
              final answers = q.answers.map((a) => [a.text, a.points]).toList();
              widget.bridge.saveQuestion(qController.text, answers, q.id);
              Navigator.of(ctx).pop();
            },
            child: const Text('Update'),
          ),
        ],
      ),
    );
  }
}
