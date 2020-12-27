<template>
  <div id="app">
    <VglRenderer camera="camera" scene="scene" style="width: 500px; height: 500px;">
      <VglShape
        :name="`cylinder${index}`"
        :path="`${line.start[0]} ${line.start[1]}, ${line.end[0]} ${line.end[1]}, ${line.end[0] + 2} ${line.end[1] + 2}, ${line.start[0] + 2} ${line.start[1] + 2}`"
        v-for="(line, index) in extrusions"
        :key="`cylinder${index}`"
        position="0 1000 0"
      />
      <VglScene name="scene">
        <VglMeshStandardMaterial
          name="mat"
          color="rgb(255, 255, 255)"
        />
        <VglPlaneGeometry
          name="bed"
          :width="1050"
          :height="350"
        />
        <VglExtrudeGeometry
          :name="`extrude${index}`"
          :shapes="`cylinder${index}`"
          :depth="1"
          v-for="(line, index) in extrusions"
          :key="`extrude${index}`"
        />
        <VglMesh
          geometry="bed"
          material="mat"
        />
        <VglGroup position="-525 -175 0">
          <VglMesh 
            :position="`0 0 ${line.layer}`"
            :geometry="`extrude${index}`" 
            material="mat" 
            v-for="(line, index) in extrusions" 
            :key="`geometry${index}`">
          </VglMesh>
        </VglGroup>
        <VglAmbientLight intensity="0.5" />
        <VglDirectionalLight
          position="0 2 1"
          intensity="0.5"
        />
      </VglScene>
      <VglPerspectiveCamera name="camera" :orbit-position="`${1000 * zoom} 2.75 0`"></VglPerspectiveCamera>
    </VglRenderer>
  </div>
</template>

<script>
import { VglRenderer, VglScene, VglShape, VglMesh, VglGroup, VglExtrudeGeometry, VglPlaneGeometry, VglPerspectiveCamera, VglMeshStandardMaterial, VglDirectionalLight, VglAmbientLight } from 'vue-gl';

export default {
  name: 'App',
  components: {
    VglExtrudeGeometry,
    VglScene,
    VglMesh,
    VglGroup,
    VglRenderer,
    VglShape,
    VglAmbientLight,
    VglPlaneGeometry,
    VglDirectionalLight,
    VglPerspectiveCamera,
    VglMeshStandardMaterial,
  },
  data() {
    return {
      extrusions: [],
      zoom: 0.25,
    };
  },
  mounted() {
    this.$options.sockets.onmessage = (message) => {this.extrusions = JSON.parse(message.data);};
    this.$options.sockets.onopen = () => this.$socket.send("init");
  }
}
</script>
