<!-- { filename: 'App.svelte' } -->
<script>
  import { LayerCake, Svg } from 'layercake';
	
  import Scatter from '$lib/components/layercake/Scatter.svelte';
  import XAxis from '$lib/components/layercake/XAxis.svelte';
  import YAxis from '$lib/components/layercake/YAxis.svelte';
  import AreaD3 from '$lib/components/layercake/AreaD3.svelte';
  import LineD3 from '$lib/components/layercake/LineD3.svelte';

	import { curveNatural } from 'd3-shape';

  const points = [
    {x: 0, y: 0},
    {x: 5, y: 20},
    {x: 6, y: 9},
    {x: 10, y: 10},
    {x: 15, y: 30},
    {x: 20, y: 40}
  ];
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
    height: 300px;
  }
</style>

<div class="chart-container">
  <LayerCake
    x='x'
    y='y'
    data={ points }
  >
    <Svg>
      <!-- You can expose properties on your chart components to make them more reusable -->
      <Scatter r={3} />
      <XAxis label="time" />
      <YAxis label="value" />
      <AreaD3 curve={curveNatural} />
      <LineD3 curve={curveNatural} />
    </Svg>
  </LayerCake>
</div>