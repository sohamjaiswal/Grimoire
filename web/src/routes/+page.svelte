<script lang="ts">
	import { page } from "$app/stores";
</script>

<h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
  Welcome to Grimoire! {$page.data.user ? `${$page.data.user.name}!` : ""}
</h1>