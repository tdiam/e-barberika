export function getCurrentDate (separator = '-') {
  let newDate = new Date()
  let date = newDate.getDate()
  let month = newDate.getMonth() + 1
  let year = newDate.getFullYear()
  if (month < 10) {
    month = `0${month}`
  }

  return `${year}${separator}${month}${separator}${date}`
}
