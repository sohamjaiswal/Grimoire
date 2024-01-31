export type CommandLog = {
  id: string,
  author: string,
  channel: string,
  command: string,
  exact: string,
  result: string,
  server: string,
  time: Date
}