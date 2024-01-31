<script lang="ts">
  import { LayerCake, Svg } from 'layercake';
  import RadialAxis from '$lib/components/layercake/RadialAxis.svelte';
	import Radar from '$lib/components/layercake/Radar.svelte';

  import Scatter from '$lib/components/layercake/Scatter.svelte';
  import XAxis from '$lib/components/layercake/XAxis.svelte';
  import YAxis from '$lib/components/layercake/YAxis.svelte';
  import AreaD3 from '$lib/components/layercake/AreaD3.svelte';
  import LineD3 from '$lib/components/layercake/LineD3.svelte';

	import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "$lib/components/ui/card";
	import Separator from "$lib/components/ui/separator/separator.svelte";

  import {db} from "$lib/utils/surreal-client";
	import { page } from '$app/stores';
	import type { CommandLog } from '$lib/types/command-log';
	import { curveLinearClosed, curveNatural } from 'd3-shape';

  import { timeParse, timeFormat } from 'd3-time-format';

  let data: Record<string, number> = {}

  const commandFrequency: Record<string, number> = {};
  const timeCast = timeParse('%Y-%m-%d-%H')
  const formatTickX = timeFormat('%Y-%m-%d:%H');
  let datedTicks: Array<Date>
  let points: Array<{x: number, y: number}> = []


  let keys: string[] = []

  const updateKeys = () => {
    keys = Object.keys(data)
  }

  $: data, updateKeys()

  const populateData = async () => {
    if ($page.data.user) {
      const commandLogRecord: Array<CommandLog[]> = await db.query(`select * from command_log where author = user:${$page.data.user.id}`)
      commandLogRecord[0].forEach((commandLog) => {
        if (data[commandLog.command]) {
          data[commandLog.command] += 1
        } else {
          data[commandLog.command] = 1
        }

        const hourDate = new Date(commandLog.time);
        hourDate.setMinutes(0);
        hourDate.setSeconds(0);
        hourDate.setMilliseconds(0);

        const hour = hourDate.getHours().toString().padStart(2, '0');
        const date = hourDate.toISOString().slice(0, 10);

        const time = `${date}-${hour}`;
        commandFrequency[time] = (commandFrequency[time] || 0) + 1;

        datedTicks = (Object.keys(commandFrequency).map((commandTime) => timeCast(commandTime)) as Array<Date>).sort((a,b) => a.getTime() - b.getTime())
        
        points = Object.keys(commandFrequency).map((time, i) => {
          return {x: i, y: commandFrequency[time]}
        })
      })
    }
  }

  const populate = populateData()
</script>

<h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
  Dashboard
</h1>
<Separator class="my-4" />
<div class="flex flex-col md:grid md:grid-cols-3 gap-4">
  <Card class="min-w-fit md:col-span-2">
    <CardHeader>
      <CardTitle>
        Power O/P:
      </CardTitle>
      <CardDescription>
        Time series visualization of power delivered...
      </CardDescription>
    </CardHeader>
    <CardContent>
      {#await populate}
        Loading Data...
      {:then}
      <div class="hidden md:block">
        <div class="freq-container">
          <LayerCake
            x='x'
            y='y'
            padding={{ top: 7, right: 10, bottom: 20, left: 25 }}
            yDomain={[0, null]}
            data={ points }
          >
            <Svg>
              <!-- You can expose properties on your chart components to make them more reusable -->
              <!-- <Scatter r={3} /> -->
              <LineD3 curve={curveNatural} />
              <AreaD3 curve={curveNatural} />
              <YAxis />
              <XAxis
              ticks={datedTicks}
              formatTick={formatTickX}
              snapTicks={true}
              tickMarks={true} />
            </Svg>
          </LayerCake>
        </div>
      </div>
      <div class="block md:hidden">
        Don't play soccer without legs...
      </div>
      {/await}
    </CardContent>
  </Card>
  <Card class="min-w-fit md:col-span-1">
    <CardHeader>
      <CardTitle>
        City Power Use:
      </CardTitle>
      <CardDescription>
        All time Power usage...
      </CardDescription>
    </CardHeader>
    <CardContent>
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
    </CardContent>
  </Card>
</div>

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
  .freq-container {
    width: 100%;
    height: 250px;
  }
</style>