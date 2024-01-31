<script>
	import Header from "$lib/components/fragments/header/header.svelte";
  import "../app.pcss";
  import { ModeWatcher } from "mode-watcher";
</script>

<ModeWatcher />
<div class="flex justify-center">
  <div class="container">
    <div class="flex flex-col items-center">
      <Header />
      <slot />
    </div>
  </div>
</div>