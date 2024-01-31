<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
-->
<script>
  import { getContext } from 'svelte';
  import { area, curveLinear } from 'd3-shape';

  import {mode} from 'mode-watcher';

  const { data, xGet, yGet, yScale } = getContext('LayerCake');

  /** @type {String} [fill='#ab00d610'] - The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let fill = "";
  const defaultFill = fill === ""
  const updateFill = () => {
    if (defaultFill) fill = $mode === 'dark' ? '#ffffff70' : '#00000030'
  }

  $: $mode, updateFill()

  /** @type {import('d3-shape').CurveFactory} [curve=curveLinear] - An optional D3 interpolation function. See [d3-shape](https://github.com/d3/d3-shape#curves) for options. Pass this function in uncalled, i.e. without the open-close parentheses. */
  export let curve = curveLinear;

  $: path = area()
    .x($xGet)
    .y1($yGet)
    .y0(d => $yScale(0))
    .curve(curve);
</script>

<path class='path-area' d='{path($data)}' {fill}></path>