class AnswerModel {
  final int id;
  final int index;
  final String text;
  final int points;
  final bool isRevealed;

  AnswerModel({
    required this.id,
    required this.index,
    required this.text,
    required this.points,
    required this.isRevealed,
  });

  factory AnswerModel.fromJson(Map<String, dynamic> json) {
    return AnswerModel(
      id: json['id'] as int? ?? 0,
      index: json['index'] as int? ?? 0,
      text: json['text'] as String? ?? '',
      points: json['points'] as int? ?? 0,
      isRevealed: json['is_revealed'] as bool? ?? false,
    );
  }
}

class QuestionModel {
  final int id;
  final String text;
  final List<AnswerModel> answers;

  QuestionModel({
    required this.id,
    required this.text,
    required this.answers,
  });

  factory QuestionModel.fromJson(Map<String, dynamic> json) {
    final rawAnswers = json['answers'] as List<dynamic>? ?? [];
    return QuestionModel(
      id: json['id'] as int? ?? 0,
      text: json['text'] as String? ?? '',
      answers: rawAnswers.map((a) => AnswerModel.fromJson(a as Map<String, dynamic>)).toList(),
    );
  }
}

class TeamModel {
  final String name;
  final int totalPoints;
  final int strikes;

  TeamModel({
    required this.name,
    required this.totalPoints,
    required this.strikes,
  });

  factory TeamModel.fromJson(Map<String, dynamic> json) {
    return TeamModel(
      name: json['name'] as String? ?? '',
      totalPoints: json['total_points'] as int? ?? 0,
      strikes: json['strikes'] as int? ?? 0,
    );
  }
}

class RoundLogModel {
  final int roundNum;
  final int teamAPoints;
  final int teamBPoints;
  final int teamAStrikes;
  final int teamBStrikes;

  RoundLogModel({
    required this.roundNum,
    required this.teamAPoints,
    required this.teamBPoints,
    required this.teamAStrikes,
    required this.teamBStrikes,
  });

  factory RoundLogModel.fromJson(Map<String, dynamic> json) {
    return RoundLogModel(
      roundNum: json['round_num'] as int? ?? 0,
      teamAPoints: json['team_a_points'] as int? ?? 0,
      teamBPoints: json['team_b_points'] as int? ?? 0,
      teamAStrikes: json['team_a_strikes'] as int? ?? 0,
      teamBStrikes: json['team_b_strikes'] as int? ?? 0,
    );
  }
}

class FastMoneyEntryModel {
  final String answer;
  final int points;
  final bool isRevealed;
  final bool isPointsRevealed;

  FastMoneyEntryModel({
    required this.answer,
    required this.points,
    required this.isRevealed,
    required this.isPointsRevealed,
  });

  factory FastMoneyEntryModel.fromJson(Map<String, dynamic> json) {
    return FastMoneyEntryModel(
      answer: json['answer'] as String? ?? '',
      points: json['points'] as int? ?? 0,
      isRevealed: json['is_revealed'] as bool? ?? false,
      isPointsRevealed: json['is_points_revealed'] as bool? ?? false,
    );
  }
}

class FastMoneyModel {
  final String teamName;
  final int timer;
  final bool isTimerRunning;
  final List<FastMoneyEntryModel> p1Entries;
  final List<FastMoneyEntryModel> p2Entries;
  final int totalPoints;

  FastMoneyModel({
    required this.teamName,
    required this.timer,
    required this.isTimerRunning,
    required this.p1Entries,
    required this.p2Entries,
    required this.totalPoints,
  });

  factory FastMoneyModel.fromJson(Map<String, dynamic> json) {
    final rawP1 = json['p1_entries'] as List<dynamic>? ?? [];
    final rawP2 = json['p2_entries'] as List<dynamic>? ?? [];
    return FastMoneyModel(
      teamName: json['team_name'] as String? ?? '',
      timer: json['timer'] as int? ?? 0,
      isTimerRunning: json['is_timer_running'] as bool? ?? false,
      p1Entries: rawP1.map((e) => FastMoneyEntryModel.fromJson(e as Map<String, dynamic>)).toList(),
      p2Entries: rawP2.map((e) => FastMoneyEntryModel.fromJson(e as Map<String, dynamic>)).toList(),
      totalPoints: json['total_points'] as int? ?? 0,
    );
  }
}

class GameStateModel {
  final int round;
  final int multiplier;
  final int bankPoints;
  final String activeScreen;
  final TeamModel teamA;
  final TeamModel teamB;
  final QuestionModel? activeQuestion;
  final int currentStrikeDisplay;
  final List<RoundLogModel> matchLog;
  final FastMoneyModel fastMoney;

  GameStateModel({
    required this.round,
    required this.multiplier,
    required this.bankPoints,
    required this.activeScreen,
    required this.teamA,
    required this.teamB,
    this.activeQuestion,
    required this.currentStrikeDisplay,
    required this.matchLog,
    required this.fastMoney,
  });

  factory GameStateModel.fromJson(Map<String, dynamic> json) {
    final qJson = json['active_question'] as Map<String, dynamic>?;
    final rawLog = json['match_log'] as List<dynamic>? ?? [];
    return GameStateModel(
      round: json['round'] as int? ?? 1,
      multiplier: json['multiplier'] as int? ?? 1,
      bankPoints: json['bank_points'] as int? ?? 0,
      activeScreen: json['active_screen'] as String? ?? 'welcome',
      teamA: TeamModel.fromJson(json['team_a'] as Map<String, dynamic>? ?? {}),
      teamB: TeamModel.fromJson(json['team_b'] as Map<String, dynamic>? ?? {}),
      activeQuestion: qJson != null ? QuestionModel.fromJson(qJson) : null,
      currentStrikeDisplay: json['current_strike_display'] as int? ?? 0,
      matchLog: rawLog.map((l) => RoundLogModel.fromJson(l as Map<String, dynamic>)).toList(),
      fastMoney: FastMoneyModel.fromJson(json['fast_money'] as Map<String, dynamic>? ?? {}),
    );
  }
}
