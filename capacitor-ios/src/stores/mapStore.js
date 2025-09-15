// stores/mapStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMapStore = defineStore('map', () => {
  // State
  const currentDataSource = ref('meta') // 'meta', 'collectionA', 'collectionB', 'collectionC'
  const mapData = ref(null)
  const metaData = ref(null) // Keep reference to original meta.json
  const collectionData = ref({
    A: null,
    B: null,
    C: null
  })
  const isLoading = ref(false)
  const error = ref(null)

  // JSON Endpoints helper
  const mapEndpoint = (path) => {
    return `${import.meta.env.VITE_API_URL}/map/${path}`
  }

  // Getters
  const currentData = computed(() => {
    switch (currentDataSource.value) {
      case 'meta':
        return metaData.value
      case 'collectionA':
        return collectionData.value.A
      case 'collectionB':
        return collectionData.value.B
      case 'collectionC':
        return collectionData.value.C
      default:
        return metaData.value
    }
  })

  const hasCollectionData = computed(() => {
    return Object.values(collectionData.value).some(data => data !== null)
  })

  // Actions
  const fetchMetaData = async () => {
    if (metaData.value) return metaData.value // Return cached data

    isLoading.value = true
    error.value = null

    try {
      const url = mapEndpoint('meta.json')
      console.log('🔡 Fetching meta data from', url)

      const response = await fetch(url)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)

      const data = await response.json()
      metaData.value = data

      // Set as current data if no other source is active
      if (currentDataSource.value === 'meta') {
        mapData.value = data
      }

      return data
    } catch (err) {
      error.value = `Failed to fetch meta data: ${err.message}`
      console.error('Meta data fetch error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchCollectionData = async (collectionId) => {
    if (collectionData.value[collectionId]) {
      return collectionData.value[collectionId] // Return cached data
    }

    isLoading.value = true
    error.value = null

    try {
      const url = mapEndpoint(`collection${collectionId}.json`)
      console.log(`🔡 Fetching collection ${collectionId} from`, url)

      const response = await fetch(url)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)

      const data = await response.json()
      collectionData.value[collectionId] = data

      return data
    } catch (err) {
      error.value = `Failed to fetch collection ${collectionId}: ${err.message}`
      console.error(`Collection ${collectionId} fetch error:`, err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const setDataSource = async (source) => {
    currentDataSource.value = source

    switch (source) {
      case 'meta':
        if (!metaData.value) {
          await fetchMetaData()
        }
        mapData.value = metaData.value
        break

      case 'collectionA':
        if (!collectionData.value.A) {
          await fetchCollectionData('A')
        }
        mapData.value = collectionData.value.A
        break

      case 'collectionB':
        if (!collectionData.value.B) {
          await fetchCollectionData('B')
        }
        mapData.value = collectionData.value.B
        break

      case 'collectionC':
        if (!collectionData.value.C) {
          await fetchCollectionData('C')
        }
        mapData.value = collectionData.value.C
        break

      default:
        console.warn(`Unknown data source: ${source}`)
    }
  }

  const resetToMeta = async () => {
    await setDataSource('meta')
  }

  const loadCollection = async (type) => {
    const collectionMap = {
      cocktail: 'collectionA',
      taco: 'collectionB',
      icecream: 'collectionC'
    }

    const dataSource = collectionMap[type]
    if (dataSource) {
      await setDataSource(dataSource)
    }
  }

  const clearError = () => {
    error.value = null
  }

  // Initialize with meta data
  const initialize = async () => {
    await fetchMetaData()
  }

  return {
    // State
    currentDataSource,
    mapData,
    metaData,
    collectionData,
    isLoading,
    error,

    // Getters
    currentData,
    hasCollectionData,

    // Actions
    fetchMetaData,
    fetchCollectionData,
    setDataSource,
    resetToMeta,
    loadCollection,
    clearError,
    initialize
  }
})