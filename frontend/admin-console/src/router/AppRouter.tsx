import { RouterProvider } from 'react-router-dom'
import router from './index'

export default function AppRouter() {
  return <RouterProvider router={router} />
}
