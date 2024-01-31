<script lang="ts">
  import 'iconify-icon'
  import {PUBLIC_CB_URL} from '$env/static/public'
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<a href={PUBLIC_CB_URL}>
  <Button class="flex gap-2" variant="outline">
    <iconify-icon icon="fa-brands:guilded" />
    Link Guilded
  </Button>
</a>