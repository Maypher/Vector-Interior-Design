import { Access } from 'payload'

const draftAccess: Access = ({ req: { user } }) => {
  if (user) return true

  // If not authenticated then return only published documents
  return {
    or: [
      {
        _status: {
          exists: false,
        },
      },
      {
        _status: {
          equals: 'published',
        },
      },
    ],
  }
}

export default draftAccess
