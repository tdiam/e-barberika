import axios from 'axios'
import qs from 'qs'


const instance = axios.create({
  // This is read from the .env file in the package root-level directory
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    common: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  },
})

const qsConfig = {
  indices: false,
}

const paramsSerializer = (params) => qs.stringify(params, qsConfig)

/**
 * API helper.
 *
 * @param {Object} args Supported parameters: { token }
 */
export default (args = {}) => {
  // If token is given as an argument, include it in the X-OBSERVATORY-AUTH header
  const { token } = args
  const reqConfig = token ? {
    headers: {
      'X-OBSERVATORY-AUTH': token,
    },
  } : {}

  // Axios by default supports only JSON requests
  // We use qs.stringify() to encode Javascript objects into URLEncoded form 'a=b&c=d'
  return {
    get: (url, params) => instance.get(url, { params, paramsSerializer, ...reqConfig }),
    post: (url, data) => instance.post(url, qs.stringify(data, qsConfig), reqConfig),
    put: (url, data) => instance.put(url, qs.stringify(data, qsConfig), reqConfig),
    patch: (url, data) => instance.patch(url, qs.stringify(data, qsConfig), reqConfig),
    delete: (url) => instance.delete(url, reqConfig),
  }
}
