<script lang="ts">
	import { page } from "$app/stores";
	import { enhance } from "$app/forms";
  
  import { Sun, Moon, Menu } from "lucide-svelte";
  import { toggleMode } from "mode-watcher";
  
  import { Button } from "$lib/components/ui/button";
	import { Separator } from "$lib/components/ui/separator";
	import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
	import { Drawer, DrawerTrigger, DrawerContent, DrawerHeader, DrawerTitle } from "$lib/components/ui/drawer";
  
  import LoginWithGuilded from "$lib/components/fragments/login-with-guilded/login-with-guilded.svelte";

  import {db} from "$lib/utils/surreal-client";
	import { onMount } from "svelte";
	import type { User } from "$lib/types/user";
	import { Popover, PopoverTrigger, PopoverContent } from "$lib/components/ui/popover";
  
  let user: User | undefined
  $: user
  onMount(async () => {
    if ($page.data.user) {
      const userRecord = await db.select(`user:${$page.data.user.id}`)
      user = userRecord[0] as User
    }
  })
</script>

<div class="w-full flex sm:hidden cannot-hover:flex my-5">
  <Drawer>
    <DrawerTrigger asChild let:builder>
      <Button builders={[builder]} variant="outline" size="icon">
        <Menu
          class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all"
        />
        <span class="sr-only">Open menu drawer</span>
      </Button>
    </DrawerTrigger>
    <DrawerContent>
      <div class="mx-auto w-full max-w-sm">
        <DrawerHeader>
          <DrawerTitle>
            <a href="/">
              Smart Grid Control
            </a>
          </DrawerTitle>
        </DrawerHeader>
        <div class="flex w-full items-center space-x-2 flex-col gap-2">
          {#if $page.data.user}
          <div class="flex flex-col items-center">
            <Avatar>
              <AvatarImage src={$page.data.user.avatar} alt={`${$page.data.user.name}'s Avatar'`} />
              <AvatarFallback>{`${$page.data.user.name.slice(0,1)}`}</AvatarFallback>
            </Avatar>
            {$page.data.user.name}
          </div>
          {/if}
          <Separator class="my-4" />
          <div class="w-[calc(100%-2rem)] flex justify-center items-center gap-4 h-5">
            <a href="/features">
              Features
            </a>
            <Separator orientation="vertical" />
            <a href="/about">
              About
            </a>
            <Separator orientation="vertical" />
            <a href="/docs">
              Docs
            </a>
          </div>
          {#if $page.data.user}
          <Separator class="my-4" />
          <div class="w-[calc(100%-2rem)] flex gap-2">
            <a class="w-1/2" href="/dashboard">
              <Button class="w-full" variant="outline">
                Dashboard
              </Button>
            </a>
            {#if user && user.role === 'ADMIN'}
            <a class="w-1/2" href="/admin">
              <Button class="w-full" variant="outline">
                Admin
              </Button>
            </a>
            {/if}
          </div>
          <Separator class="my-4" />
          <form class="w-full flex gap-2 justify-center pb-2" action="/logout" method="post" use:enhance>
            <Button on:click={toggleMode} variant="outline" size="icon">
              <Sun
              class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
              />
              <Moon
              class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
              />
              <span class="sr-only">Toggle theme</span>
            </Button>
            <Button class="flex gap-2 w-[calc(100%-5rem)]" variant="outline" type='submit'>
              <iconify-icon icon="fa-solid:sign-out-alt" />
              Logout
            </Button>
          </form>
          {:else}
          <Separator class="my-4" />
          <div class="w-full flex gap-2 jusify-center pb-2">
            <Button on:click={toggleMode} variant="outline" size="icon">
              <Sun
                class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
              />
              <Moon
                class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
              />
              <span class="sr-only">Toggle theme</span>
            </Button>
            <LoginWithGuilded />
          </div>
          {/if}
        </div>
      </div>
    </DrawerContent>
  </Drawer>
</div>

<div class="hidden sm:flex cannot-hover:hidden w-full my-5 p-2 py-1 justify-between items-center rounded-md ring-offset-background border">
  <a href="/" class="w-1/3">
    <h1 class="tracking-tight">
      <strong>
        Smart Grid Control
      </strong>
    </h1>
  </a>
  <div class="flex items-center justify-center min-w-fit w-1/3 h-5 gap-2">
    <a href="/features">Features</a>
    <Separator orientation="vertical" />
    <a href="/about">About</a>
    <Separator orientation="vertical" />
    <a href="/docs">Docs</a>
  </div>
  <div class="flex justify-end items-center gap-4 w-1/3">
    {#if $page.data.user}
    <Popover>
      <PopoverTrigger>
        <Avatar>
          <AvatarImage src={$page.data.user.avatar} alt={`${$page.data.user.name}'s Avatar'`} />
          <AvatarFallback>{`${$page.data.user.name.slice(0,1)}`}</AvatarFallback>
        </Avatar>
      </PopoverTrigger>
      <PopoverContent>
        <div class="flex flex-col items-center gap-4">
          <div class="w-[calc(100%-2rem)] flex flex-col gap-2">
            <a class="w-full" href="/dashboard">
              <Button class="w-full" variant="outline">
                Dashboard
              </Button>
            </a>
            {#if user && user.role === 'ADMIN'}
            <a class="w-full" href="/admin">
              <Button class="w-full" variant="outline">
                Admin
              </Button>
            </a>
            {/if}
          </div>
          <Separator class="my-4" />
          <form class="w-full flex gap-2 justify-center" action="/logout" method="post" use:enhance>
            <Button on:click={toggleMode} variant="outline" size="icon">
              <Sun
                class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
              />
              <Moon
                class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
              />
              <span class="sr-only">Toggle theme</span>
            </Button>
            <Button class="flex gap-2 w-[calc(100%-5rem)]" variant="outline" type='submit'>
              <iconify-icon icon="fa-solid:sign-out-alt" />
              Logout
            </Button>
          </form>
        </div>
      </PopoverContent>
    </Popover>
    {:else}
    <div class="w-full flex gap-2 justify-end">
      <Button on:click={toggleMode} variant="outline" size="icon">
        <Sun
          class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
        />
        <Moon
          class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
        />
        <span class="sr-only">Toggle theme</span>
      </Button>
      <LoginWithGuilded />
    </div>
    {/if}
  </div>
</div>
