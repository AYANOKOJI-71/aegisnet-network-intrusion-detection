export function titleCase(value: string): string {
  return value.replaceAll("-", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function formatTimestamp(value: string): string {
  return new Date(value).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export function formatBytes(value: number): string {
  return value >= 1024 ? `${(value / 1024).toFixed(1)} KB` : `${value} B`;
}
