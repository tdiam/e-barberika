import axios from 'axios'
import qs from 'qs'

const instance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    headers: {
        common: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }
})

const qsConfig = {
    indices: false
}

export default {
    get: (url, params) => instance.get(url, { params }),
    post: (url, data) => instance.post(url, qs.stringify(data, qsConfig)),
    put: (url, data) => instance.put(url, qs.stringify(data, qsConfig)),
    patch: (url, data) => instance.patch(url, qs.stringify(data, qsConfig)),
    delete: (url) => instance.delete(url),
}