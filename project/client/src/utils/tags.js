export function tagsToText(tags) {
  if (tags && tags.length > 0) {
    let res = tags[0]
    tags.slice(1, tags.length).forEach(x => {
      res += ", " + x
    })
    return res
  }
  return ""
}

export function textToTags(tags) {
  let arr = tags.split(',')
  let res = []
  arr.forEach(x => {
    x = x.trim();
    if (x.length > 0 && x.trim() !== '') res.push(x.trim())
  })
  return res
}