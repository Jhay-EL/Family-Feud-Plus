import 'dart:async';
import 'package:flutter/material.dart';
import '../../../core/constants/game_colors.dart';
import '../../../core/models/game_models.dart';
import '../../../core/services/game_bridge.dart';

class FastMoneyTab extends StatefulWidget {
  final GameBridgeService bridge;
  final GameStateModel? state;

  const FastMoneyTab({
    Key? key,
    required this.bridge,
    required this.state,
  }) : super(key: key);

  @override
  State<FastMoneyTab> createState() => _FastMoneyTabState();
}

class _FastMoneyTabState extends State<FastMoneyTab> {
  String _selectedTeam = 'Choose Team';
  final TextEditingController _timerController = TextEditingController(text: '20');
  int _remainingTimer = 0;
  Timer? _countdownTimer;

  // Controllers for Player 1 & Player 2 inputs
  final List<TextEditingController> _p1AnswerControllers = List.generate(5, (_) => TextEditingController());
  final List<TextEditingController> _p1PointControllers = List.generate(5, (_) => TextEditingController());
  final List<TextEditingController> _p2AnswerControllers = List.generate(5, (_) => TextEditingController());
  final List<TextEditingController> _p2PointControllers = List.generate(5, (_) => TextEditingController());

  @override
  void initState() {
    super.initState();
    _syncInputsFromState();
  }

  @override
  void didUpdateWidget(covariant FastMoneyTab oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.state != widget.state) {
      _syncInputsFromState();
    }
  }

  void _syncInputsFromState() {
    if (widget.state != null) {
      final fm = widget.state!.fastMoney;
      for (int i = 0; i < 5; i++) {
        if (i < fm.p1Entries.length) {
          if (_p1AnswerControllers[i].text.isEmpty && fm.p1Entries[i].answer.isNotEmpty) {
            _p1AnswerControllers[i].text = fm.p1Entries[i].answer;
          }
          if (_p1PointControllers[i].text.isEmpty && fm.p1Entries[i].points > 0) {
            _p1PointControllers[i].text = '${fm.p1Entries[i].points}';
          }
        }
        if (i < fm.p2Entries.length) {
          if (_p2AnswerControllers[i].text.isEmpty && fm.p2Entries[i].answer.isNotEmpty) {
            _p2AnswerControllers[i].text = fm.p2Entries[i].answer;
          }
          if (_p2PointControllers[i].text.isEmpty && fm.p2Entries[i].points > 0) {
            _p2PointControllers[i].text = '${fm.p2Entries[i].points}';
          }
        }
      }
    }
  }

  void _startTimer() {
    _countdownTimer?.cancel();
    final sec = int.tryParse(_timerController.text) ?? 20;
    setState(() {
      _remainingTimer = sec;
    });

    widget.bridge.playAudio('fm_count');

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
    _timerController.dispose();
    for (var c in _p1AnswerControllers) c.dispose();
    for (var c in _p1PointControllers) c.dispose();
    for (var c in _p2AnswerControllers) c.dispose();
    for (var c in _p2PointControllers) c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.state == null) {
      return const Center(child: CircularProgressIndicator());
    }

    final state = widget.state!;
    final fm = state.fastMoney;

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ================= COLUMN 1: QUESTION VIEW, DB TOOLS =================
          Expanded(
            flex: 32,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Select team to play the Fast Money round',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 6),
                  Container(
                    height: 38,
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      border: Border.all(color: GameColors.gameGreen, width: 2),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: DropdownButtonHideUnderline(
                      child: DropdownButton<String>(
                        isExpanded: true,
                        value: _selectedTeam,
                        items: [
                          const DropdownMenuItem(value: 'Choose Team', child: Text('Choose Team')),
                          DropdownMenuItem(
                            value: state.teamA.name,
                            child: Text(state.teamA.name.isNotEmpty ? state.teamA.name : 'Team A'),
                          ),
                          DropdownMenuItem(
                            value: state.teamB.name,
                            child: Text(state.teamB.name.isNotEmpty ? state.teamB.name : 'Team B'),
                          ),
                        ],
                        onChanged: (val) {
                          if (val != null) {
                            setState(() {
                              _selectedTeam = val;
                            });
                          }
                        },
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),

                  const Text(
                    'Game questions view',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 6),
                  Container(
                    width: double.infinity,
                    height: 100,
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: const Color(0xFFC0C0C0),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: Colors.grey.shade500),
                    ),
                    alignment: Alignment.centerLeft,
                    child: const Text(
                      'Fast Money Question Display Area',
                      style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.black87),
                    ),
                  ),
                  const SizedBox(height: 14),

                  const Text(
                    'Click the answer button to reveal to the Fast Money round window',
                    style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 6),
                  for (int i = 1; i <= 5; i++)
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 3.0),
                      child: Row(
                        children: [
                          Expanded(
                            child: Container(
                              height: 32,
                              alignment: Alignment.centerLeft,
                              padding: const EdgeInsets.symmetric(horizontal: 8),
                              decoration: BoxDecoration(
                                color: const Color(0xFFC0C0C0),
                                borderRadius: BorderRadius.circular(3),
                              ),
                              child: Text('Answer $i', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                            ),
                          ),
                          const SizedBox(width: 6),
                          Container(
                            width: 50,
                            height: 32,
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              color: const Color(0xFFC0C0C0),
                              borderRadius: BorderRadius.circular(3),
                            ),
                            child: const Text('0', style: TextStyle(fontFamily: 'Consolas', fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                    ),
                  const SizedBox(height: 16),

                  const Text(
                    'Add or load questions and answer to the database',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: _buildButton('Load from file', GameColors.gameGreen, () {}),
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: _buildButton('Manual Add questions', GameColors.gameGreen, () {}),
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: _buildButton('Save', GameColors.gameGreen, () {}),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),

                  const Text(
                    'Edit questions and answers from the database',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: _buildButton('Modify', GameColors.gameGreen, () {}),
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: _buildButton('Save', GameColors.gameGreen, () {}),
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: _buildButton('Delete', GameColors.strikeRed, () {}),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 16),

          // ================= COLUMN 2: CONTESTANT ANSWERS (PLAYER 1 & 2) =================
          Expanded(
            flex: 44,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Contestant answers',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 8),

                  // Player 1 Section
                  const Text(
                    'Player 1 answers',
                    style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 4),
                  for (int i = 0; i < 5; i++)
                    _buildContestantRow(1, i, _p1AnswerControllers[i], _p1PointControllers[i], fm.p1Entries),

                  const SizedBox(height: 14),

                  // Player 2 Section
                  const Text(
                    'Player 2 answers',
                    style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 4),
                  for (int i = 0; i < 5; i++)
                    _buildContestantRow(2, i, _p2AnswerControllers[i], _p2PointControllers[i], fm.p2Entries),

                  const SizedBox(height: 14),

                  // Total Points Display
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      const Text(
                        'Total:',
                        style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                      ),
                      const SizedBox(width: 10),
                      Container(
                        width: 70,
                        height: 34,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: const Color(0xFFC0C0C0),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          '${fm.totalPoints}',
                          style: const TextStyle(
                            fontFamily: 'Consolas',
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),

                  // Timer & Winning Answer Sound Controls
                  Row(
                    children: [
                      // Set timer group
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Set timer to the game',
                            style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                          ),
                          const SizedBox(height: 4),
                          Row(
                            children: [
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
                              const SizedBox(width: 8),
                              SizedBox(
                                height: 32,
                                child: ElevatedButton(
                                  onPressed: _remainingTimer > 0 ? null : _startTimer,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: _remainingTimer > 0 ? GameColors.cautionOrange : GameColors.gameGreen,
                                    padding: const EdgeInsets.symmetric(horizontal: 14),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
                                  ),
                                  child: Text(
                                    _remainingTimer > 0 ? 'Timer: $_remainingTimer' : 'Start timer',
                                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                      const Spacer(),

                      // Winning Answer Sound Button
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Winning Answer Sound',
                            style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                          ),
                          const SizedBox(height: 4),
                          SizedBox(
                            height: 32,
                            child: ElevatedButton(
                              onPressed: () => widget.bridge.playAudio('win_sound'),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: GameColors.gameGreen,
                                padding: const EdgeInsets.symmetric(horizontal: 14),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
                              ),
                              child: const Text('Winning Answer Sound', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 16),

          // ================= COLUMN 3: QUEUED QUESTIONS & RESET =================
          Expanded(
            flex: 24,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Queued questions',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: GameColors.primaryBlue),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    height: 380,
                    decoration: BoxDecoration(
                      color: const Color(0xFFC0C0C0),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: Colors.grey.shade500),
                    ),
                    child: ListView(
                      padding: const EdgeInsets.all(8),
                      children: const [
                        Text('Question 1', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Question 2', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Question 3', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Question 4', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Question 5', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  _buildButton('Start Over', GameColors.strikeRed, () => widget.bridge.resetFastMoney()),
                  const SizedBox(height: 8),
                  _buildButton('Clear questions', GameColors.strikeRed, () => widget.bridge.sendAction('CLEAR_QUESTIONS')),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildContestantRow(
    int playerNum,
    int index,
    TextEditingController answerCtrl,
    TextEditingController pointCtrl,
    List<FastMoneyEntryModel> entries,
  ) {
    final entry = index < entries.length ? entries[index] : null;
    final isAnswerRevealed = entry?.isRevealed ?? false;
    final isPointsRevealed = entry?.isPointsRevealed ?? false;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0),
      child: Row(
        children: [
          // Answer text input
          Expanded(
            child: Container(
              height: 30,
              decoration: BoxDecoration(
                color: const Color(0xFFE8E8E8),
                borderRadius: BorderRadius.circular(3),
                border: Border.all(color: Colors.grey.shade400),
              ),
              child: TextField(
                controller: answerCtrl,
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                decoration: const InputDecoration(
                  contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                  border: InputBorder.none,
                ),
                onSubmitted: (val) {
                  final pts = int.tryParse(pointCtrl.text) ?? 0;
                  widget.bridge.setFastMoneyEntry(playerNum, index, val, pts);
                },
              ),
            ),
          ),
          const SizedBox(width: 4),

          // Answer Reveal Button
          SizedBox(
            width: 58,
            height: 30,
            child: ElevatedButton(
              onPressed: () {
                final pts = int.tryParse(pointCtrl.text) ?? 0;
                widget.bridge.setFastMoneyEntry(playerNum, index, answerCtrl.text, pts);
                widget.bridge.revealFastMoneyAnswer(playerNum, index);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: isAnswerRevealed ? GameColors.primaryBlue : const Color(0xFFC0C0C0),
                foregroundColor: isAnswerRevealed ? Colors.white : Colors.black87,
                padding: EdgeInsets.zero,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
              ),
              child: Text(
                isAnswerRevealed ? 'Shown' : 'Reveal',
                style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          const SizedBox(width: 6),

          // Points input
          Container(
            width: 45,
            height: 30,
            decoration: BoxDecoration(
              color: const Color(0xFFE8E8E8),
              borderRadius: BorderRadius.circular(3),
              border: Border.all(color: Colors.grey.shade400),
            ),
            child: TextField(
              controller: pointCtrl,
              textAlign: TextAlign.center,
              keyboardType: TextInputType.number,
              style: const TextStyle(fontFamily: 'Consolas', fontSize: 12, fontWeight: FontWeight.bold),
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.zero,
                border: InputBorder.none,
              ),
              onSubmitted: (val) {
                final pts = int.tryParse(val) ?? 0;
                widget.bridge.setFastMoneyEntry(playerNum, index, answerCtrl.text, pts);
              },
            ),
          ),
          const SizedBox(width: 4),

          // Points Reveal Button
          SizedBox(
            width: 58,
            height: 30,
            child: ElevatedButton(
              onPressed: () {
                final pts = int.tryParse(pointCtrl.text) ?? 0;
                widget.bridge.setFastMoneyEntry(playerNum, index, answerCtrl.text, pts);
                widget.bridge.revealFastMoneyPoints(playerNum, index);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: isPointsRevealed ? GameColors.gameGreen : const Color(0xFFC0C0C0),
                foregroundColor: isPointsRevealed ? Colors.white : Colors.black87,
                padding: EdgeInsets.zero,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
              ),
              child: Text(
                isPointsRevealed ? 'Shown' : 'Reveal',
                style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildButton(String label, Color color, VoidCallback onPressed) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        minimumSize: const Size.fromHeight(32),
        padding: const EdgeInsets.symmetric(horizontal: 6),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
      ),
      child: Text(
        label,
        style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
        textAlign: TextAlign.center,
      ),
    );
  }
}
