import React, { Component } from 'react'

import { tagsToText, textToTags } from '../utils/tags'

class TagInput extends Component {
  constructor (props) {
    super(props)
    this.state = {
      raw: tagsToText(this.props.value),
    }
  }

  handleChange = (e) => {
    this.setState({
      raw: e.target.value,
    })
    this.props.onChange(textToTags(e.target.value))
  }

  render() {
    const { tag: Tag, onChange, ...restProps } = this.props
    return (
      <Tag { ...restProps } type="text" onChange={ this.handleChange } value={ this.state.raw } />
    )
  }
}
TagInput.defaultProps = {
  tag: 'input',
}

export default TagInput
