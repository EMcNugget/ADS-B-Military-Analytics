// Gets the previous Sunday for EOW stats
export const getSunday = (date: string) => {
  const givenDate = new Date(date);
  const dayOfWeek = givenDate.getDay();
  const previousSundayDate = new Date(
    givenDate.getFullYear(),
    givenDate.getMonth(),
    givenDate.getDate() - dayOfWeek
  );
  return previousSundayDate.toISOString().split("T")[0];
};

// Gets the first day of the month for EOM stats
export const getMonth = (date: string) => {
  const given = new Date(date);
  const firstDayOfMonth = new Date(given.getFullYear(), given.getMonth(), 1);
  return firstDayOfMonth.toISOString().split("T")[0];
};

