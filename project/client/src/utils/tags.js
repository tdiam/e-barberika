export function tagsToText(tags) {
  return tags ? tags.join(', ') : ''
}

export function textToTags(text) {
  return text ? text.split(',').map(t => t.trim()).filter(t => t !== '') : []
}
