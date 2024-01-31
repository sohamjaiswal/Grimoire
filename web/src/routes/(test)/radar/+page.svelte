<script lang="ts">
  import { LayerCake, Svg } from 'layercake';

  // This example loads csv data as json using @rollup/plugin-dsv
	import RadialAxis from '$lib/components/layercake/RadialAxis.svelte';
	import Radar from '$lib/components/layercake/Radar.svelte';
	import { curveLinearClosed } from 'd3-shape';

  const data = {
    fastball: 10,
    change: 4,
    slider: 6,
    cutter: 8,
    curve: 5
  };

  const keys: string[] = Object.keys(data);
</script>

<style>
  /*
    The wrapper div needs to have an explicit width and height in CSS.
    It can also be a flexbox child or CSS grid element.
    The point being it needs dimensions since the <LayerCake> element will
    expand to fill it.
  */
  .chart-container {
    width: 100%;
    height: 250px;
  }
</style>

<div class="chart-container">
  <LayerCake
    padding={{ top: 30, right: 0, bottom: 7, left: 0 }}
    x={keys}
    xDomain={[0, 10]}
    xRange={({height}) => [0, height / 2]}
    data={[data]}
  >
    <Svg>
      <RadialAxis/>
      <Radar curve={curveLinearClosed}/>
    </Svg>
  </LayerCake>
</div>