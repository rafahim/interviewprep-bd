export type SM2State = {
  repetitions: number;
  interval: number;
  easeFactor: number;
  nextReview: string | null;
};

export function calculateSM2(previous: SM2State, rating: number, now = new Date()): SM2State {
  const quality = Math.max(0, Math.min(5, Math.round(rating)));
  let repetitions = previous.repetitions;
  let interval = previous.interval;
  let easeFactor = previous.easeFactor || 2.5;
  if (quality < 3) {
    repetitions = 0;
    interval = 1;
  } else {
    if (repetitions === 0) interval = 1;
    else if (repetitions === 1) interval = 6;
    else interval = Math.max(1, Math.round(interval * easeFactor));
    repetitions += 1;
  }
  easeFactor = Math.max(1.3, easeFactor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  const next = new Date(now);
  next.setDate(next.getDate() + interval);
  return { repetitions, interval, easeFactor, nextReview: next.toISOString() };
}
