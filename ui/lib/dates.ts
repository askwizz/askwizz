import { DateTime } from "luxon";

export const formatDate = (date: string) => {
  return DateTime.fromISO(date).toLocaleString(DateTime.DATETIME_SHORT);
};
