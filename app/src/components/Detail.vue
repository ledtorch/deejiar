<template>
  <div class="body">
    <div class="cover" :style="{ 'backgroundImage': mainColumnImage }"></div>
    <div class="content">
      <div class=" content-frame">
        <div class="title-block">
          <h2 class="stretch">{{ storeTitle }}</h2>
          <TagShopType :store="dataFromBottomSheet" />
        </div>
        <p class="state">{{ description }}</p>
        <p>{{}}</p>
      </div>
    </div>
  </div>
</template>
  
<script>
import IconButtonClose from "./Button/IconButtonClose.vue";
import TagShopType from "./Button/TagShopType.vue";
import Review from "./Sheet/Review.vue";
import Businesshour from "./Sheet/Businesshour.vue";

export default {
  components: { IconButtonClose, TagShopType, Review, Businesshour },
  data() {
    return {
      storeTitle: '',
      description: '',
      storeType: ''
    }
  },
  props: {
    title: String,
    dataFromBottomSheet: Object,
  },
  methods: {
    backgroundImageUrl(imagePath) {
      const baseUrl = `${window.location.protocol}//${window.location.host}`;
      return `url('${baseUrl}/${imagePath}')`;
    }
  },

  computed: {

    storeLayout() {
      // // 🐞 Debug console
      // console.log("Compute storeLayout: " + this.store?.layout);
      return this.dataFromBottomSheet?.layout;
    },

    mainColumnImage() {
      return this.backgroundImageUrl(this.dataFromBottomSheet.storefront);
    },
    item1() {
      return this.backgroundImageUrl(this.dataFromBottomSheet?.item1.image);
    },
    item2() {
      return this.backgroundImageUrl(this.dataFromBottomSheet?.item2.image);
    },
    item3() {
      return this.backgroundImageUrl(this.dataFromBottomSheet?.item3.image);
    },
    item4() {
      return this.backgroundImageUrl(this.dataFromBottomSheet?.item4.image);
    },
    item5() {
      return this.backgroundImageUrl(this.dataFromBottomSheet?.item5.image);
    }
  },
  mounted() {
    this.storeTitle = this.title;
    this.description = this.dataFromBottomSheet.description;
    this.storeType = this.dataFromBottomSheet.type;

    // // 🐞 Debug console
    // console.log("The Data in Detail.vue");
    // console.log("dataFromBottomSheet:", this.dataFromBottomSheet);
    // console.log("title:", this.title);
    // console.log('storeType:', this.storeType);
  },
};

</script>

<style lang="scss" scoped>
.body {
  position: relative;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
}

.content {
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  height: 100%;
  padding: 20px;
  gap: 24px;
}

.title-block {
  align-items: flex-start;
  justify-content: flex-start;
  align-content: flex-start;
  align-self: stretch;
  flex-wrap: wrap;
  flex: 1 0 0;
  gap: 12px;
}

.cover {
  align-items: center;
  width: 100%;
  height: 100%;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}


.stretch {
  flex: 1 0 0;
}

.content-frame {
  flex-direction: column;
  gap: 12px;
}

.state {
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  padding: 12px;
  border-radius: var(--border-button-round, 8px);
  background: var(--4-base-dark-base, rgba(255, 255, 255, 0.07));
}
</style>
  