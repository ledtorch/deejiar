// stores/mapStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMapStore = defineStore('map', () => {
  // ===========================
  // Core Map State
  // ===========================
  const currentDataSource = ref('meta') // 'meta', 'collectionA', 'collectionB', 'collectionC'
  const mapData = ref(null)

  // ===========================
  // Navigation Action
  // ===========================
  const navigateToLocation = ref({
    coordinates: null,
    zoomLevel: null
  })

  // Map render json
  const metaData = ref(null) // Keep reference to original meta.json
  const collectionData = ref({
    A: null,
    B: null,
    C: null
  })

  const isLoading = ref(false)
  const error = ref(null)

  // ===========================
  // TagFilter State Management
  // ===========================
  const showTagFilter = ref(false)
  const activeCollectionType = ref(null) // 'cocktail', 'icecream', 'taco'

  // ===========================
  // Utilities
  // ===========================
  const mapEndpoint = (path) => {
    return `${import.meta.env.VITE_API_URL}/map/${path}?v=${Date.now()}`
  }

  // ===========================
  // Computed Properties
  // ===========================
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

  // ===========================
  // Core Map Actions
  // ===========================
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

  // ===========================
  // TagFilter Actions
  // ===========================
  const setTagFilter = (collectionType) => {
    activeCollectionType.value = collectionType
    showTagFilter.value = true
  }

  const hideTagFilter = () => {
    showTagFilter.value = false
    activeCollectionType.value = null
  }

  // ===========================
  // Combined Actions
  // ===========================
  const resetToMeta = async () => {
    await setDataSource('meta')
    hideTagFilter() // Hide TagFilter when resetting to meta
  }

  const loadCollection = async (type) => {
    const collectionMap = {
      cocktail: 'collectionA',
      icecream: 'collectionB',
      taco: 'collectionC'
    }

    const dataSource = collectionMap[type]
    if (dataSource) {
      await setDataSource(dataSource)
      setTagFilter(type) // Show TagFilter when loading collection
    }
  }

  // ===========================
  // Utility Actions
  // ===========================
  const clearError = () => {
    error.value = null
  }

  const initialize = async () => {
    await fetchMetaData()
  }

  return {
    // Core State
    currentDataSource,
    mapData,
    metaData,
    collectionData,
    isLoading,
    error,

    // TagFilter State
    showTagFilter,
    activeCollectionType,

    // Computed Properties
    currentData,
    hasCollectionData,

    navigateToLocation,

    // Core Actions
    fetchMetaData,
    fetchCollectionData,
    setDataSource,
    resetToMeta,
    loadCollection,
    clearError,
    initialize,

    // TagFilter Actions
    setTagFilter,
    hideTagFilter
  }
})