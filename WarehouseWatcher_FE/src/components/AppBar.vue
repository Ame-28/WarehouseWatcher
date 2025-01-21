<!-- 
 FILE: AppBar.vue
 PROJECT: Warehouse Watcher
 PROGRAMMER: Undefined Chargers - Yujung Park
 FIRST VERSION: 2025-01-10
 DESCRIPTION: 
 References: Starting code- https://vuetifyjs.com/en/components/app-bars/#images
 -->

 <template>
    <v-card class="mx-auto" color="indigo-darken-4" max-width="448">
      <v-layout>
        <v-app-bar
          color="#021324"
        >
  
          <template v-slot:prepend>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>
          </template>
  
          <v-app-bar-title @click="$router.push({path:'/'})">WAREHOUSE WATCHER</v-app-bar-title>
  
          <v-spacer></v-spacer>
          <v-btn @click="$router.push({path:'/dashboard'})"> 
            Dashboard
          </v-btn>
          <v-btn @click="$router.push({path:'/space'})"> 
            Space
          </v-btn>
          <v-btn @click="$router.push({path:'/about'})">
            About
          </v-btn>
  
          <!-- <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
  
          <v-btn icon>
            <v-icon>mdi-heart</v-icon>
          </v-btn>
  
          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn> -->
        </v-app-bar>
  
      </v-layout>
    </v-card>
  </template>