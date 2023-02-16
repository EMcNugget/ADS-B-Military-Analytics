import React from 'react'
import ReactDOM from 'react-dom/client'
import Api from './api_fetch'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Api />
  </React.StrictMode>,
)
