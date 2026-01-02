export const ROBOTS = Object.freeze({
  BB016: "BB016",
  BB011: "BB011",
  BB046: "BB046",
});

export async function getRobots() {
  const robots = await fetch('/api/robots');

  return await robots.json();
}
