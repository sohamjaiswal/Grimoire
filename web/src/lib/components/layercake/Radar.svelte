<!--
  @component
  Generates an SVG radar chart.
 -->
 <script>
  import { getContext } from 'svelte';
  import { line, curveCardinalClosed } from 'd3-shape';

  import {mode} from 'mode-watcher';

  const { data, width, height, xGet, config } = getContext('LayerCake');

  /**  @type {Number} [stroke=2] The radar's stroke color. */
  export let strokeWidth = 2

  /**  @type {String} [fill='#f0c'] The radar's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let fill = "";
  const defaultFill = fill === ""
  const updateFill = () => {
    if (defaultFill && strokeWidth > 0) fill = $mode === 'dark' ? '#000000' : '#ffffff'
    else if (defaultFill) fill = $mode === 'dark' ? '#ffffff' : '#000000'
  }

  /**  @type {String} [stroke='#f0c'] The radar's stroke color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let stroke = "";
  const defaultStroke = stroke === ""
  const updateStroke = () => {
    if (defaultStroke) stroke = $mode === 'dark' ? '#ffffff' : '#000000'
  }

  /**  @type {Number} [fillOpacity=0.5] The radar's fill opacity. */
  export let fillOpacity = 0.5

  /**  @type {Number} [r=4.5] Each circle's radius. */
  export let r = 4.5;
  
  /**  @type {Number} [circleStrokeWidth=1] Each circle's stroke width. */
  export let circleStrokeWidth = 1;

  /**  @type {String} [circleFill="#f0c"] Each circle's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let circleFill = "";
  const defaultCircleFill = circleFill === ""
  const updateCircleFill = () => {
    if (defaultCircleFill && circleStrokeWidth > 0) circleFill = $mode === 'dark' ? '#000000' : '#ffffff'
    else if (defaultCircleFill) circleFill = $mode === 'dark' ? '#ffffff' : '#000000'
  }

  /**  @type {String} [circleStroke="#fff"] Each circle's stroke color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let circleStroke = "";
  const defaultCircleStroke = circleStroke === ""
  const updateCircleStroke = () => {
    if (defaultCircleStroke) circleStroke = $mode === 'dark' ? '#ffffff' : '#000000'
  }
  
  /** @type {import('d3-shape').CurveFactory | import('d3-shape').CurveFactoryLineOnly} [curve=curveLinear] - An optional D3 interpolation function. See [d3-shape](https://github.com/d3/d3-shape#curves) for options. Pass this function in uncalled, i.e. without the open-close parentheses. */
  export let curve = curveCardinalClosed

  $: $mode, updateCircleStroke(), updateCircleFill(), updateStroke(), updateFill()

  $: angleSlice = (Math.PI * 2) / $config.x.length;

  $: path = line()
    .curve(curve)
    // @ts-ignore
    .x((d, i) => d * Math.cos(angleSlice * i - Math.PI / 2))
    // @ts-ignore
    .y((d, i) => d * Math.sin(angleSlice * i - Math.PI / 2));
</script>

{#key $mode}
<g
  transform="translate({ $width / 2 }, { $height / 2 })"
>
  {#each $data as row}
    {@const xVals = $xGet(row)}
    <!-- Draw a line connecting all the dots -->
    <path
      class='path-line'
      d='{path(xVals)}'
      stroke="{stroke}"
      stroke-width="{strokeWidth}"
      fill="{fill}"
      fill-opacity="{fillOpacity}"
    ></path>

    <!-- Plot each dots -->
    {#each xVals as circleR, i}
      {@const thisAngleSlice = angleSlice * i - Math.PI / 2}
      <circle
        cx={circleR * Math.cos(thisAngleSlice)}
        cy={circleR * Math.sin(thisAngleSlice)}
        r="{r}"
        fill="{circleFill}"
        stroke="{circleStroke}"
        stroke-width="{circleStrokeWidth}"
      ></circle>
    {/each}
  {/each}
</g>
{/key}

<style>
  .path-line {
    stroke-linejoin: round;
    stroke-linecap: round;
  }
</style>