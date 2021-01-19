<template>
  <div id="app">
    {{ this.extrusionsData[0] ? this.extrusionsData[0].temperature_value_history : '' }}
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
        <VglMeshStandardMaterial
          name="mat-black"
          color="rgb(0, 0, 0)"
        />
        <VglMeshStandardMaterial
          :name="`mat${matNo}`"
          :color="`rgb(${17*matNo}, 0, ${255 - 17*matNo})`"
          v-for="matNo in Array(16).keys()"
          :key="matNo"
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
            :material="line.colour != 0 ? (line.colour <= 15 ? `mat${line.colour}` : 'mat15') : 'mat-black'" 
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
      extrusionsData: [],
      zoom: 0.25,
    };
  },
  computed: {
    maxTemp() {
      return 100;
      //return Math.max(...this.extrusionsData.map(x => x.temperature_values).flat());
    },
    minTemp() {
      return 20;
      //return Math.min(...this.extrusionsData.map(x => x.temperature_values).flat().filter(x => x != 0));
    },
    extrusions() {
      return this.extrusionsData.map(extrusion => {
        const deltaX = extrusion.end[0] - extrusion.start[0];
        const deltaY = extrusion.end[1] - extrusion.start[1];
        const xStep = deltaX / extrusion.temperature_values.length;
        const yStep = deltaY / extrusion.temperature_values.length;
        return extrusion.temperature_values.map((temperature, index) => ({
          layer: extrusion.layer,
          start: [
            extrusion.start[0] + xStep * (index), 
            extrusion.start[1] + yStep * (index)
          ],
          end: [
            extrusion.start[0] + xStep * (index + 1), 
            extrusion.start[1] + yStep * (index + 1)
          ],
          colour: temperature == 0 ? 0 : parseInt(((temperature - this.minTemp)/(this.maxTemp - this.minTemp))*15),
        }));
      }).flat();
    }
  },
  mounted() {
    this.$options.sockets.onmessage = (message) => {this.extrusionsData = JSON.parse(message.data);};
    this.$options.sockets.onopen = () => this.$socket.send("init");
  }
}
</script>
