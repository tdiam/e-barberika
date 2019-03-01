export function getCurrentDate (separator = '-') {
  let newDate = new Date()
  let date = newDate.getDate()
  if (date < 10) {
    date = `0${date}`
  }
  let month = newDate.getMonth() + 1
  let year = newDate.getFullYear()
  if (month < 10) {
    month = `0${month}`
  }

  return `${year}${separator}${month}${separator}${date}`
}
