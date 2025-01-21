// FILE: WarehouseScene.js
// PROJECT: Warehouse Watcher
// PROGRAMMER: Undefined Chargers - Yujung Park
// FIRST VERSION: 2025-01-10
// DESCRIPTION:
// References: 
// https://doc.babylonjs.com/communityExtensions/Babylon.js+ExternalLibraries/BabylonJS_and_Vue/BabylonJS_and_Vue_1#vue-3
// https://www.youtube.com/watch?v=NLZuUtiL50A&list=PLym1B0rdkvqhuCNSXzxw6ofEkrpYI70P4

import { Engine, Scene, FreeCamera, Vector3, MeshBuilder, StandardMaterial, Color3, HemisphericLight, SceneLoader } from "@babylonjs/core";
import "@babylonjs/loaders"
import "@babylonjs/core/Debug/debugLayer";
import { Inspector } from '@babylonjs/inspector';

export class WarehouseScene {
  scene: Scene;
  engine: Engine;

  constructor(private canvas: HTMLCanvasElement) {
    this.engine = new Engine(this.canvas, true);
    this.scene = this.CreateScene();

    this.engine.runRenderLoop(() => {
      this.scene.render();
    });
  }
  
  CreateScene(): Scene {
    const scene = new Scene(this.engine);
    const camera = new FreeCamera("camera", new Vector3(15, 10, 8), this.scene);
    camera.attachControl();
    camera.speed = 0.25;

    const hemiLight = new HemisphericLight(
      "hemiLight",
      new Vector3(0, 1, 0),
      this.scene
    );

    hemiLight.intensity = 1.5;

    camera.setTarget(new Vector3(-9.32, 3.95, -1.07));

    this.LoadModels();



    return scene;
  }

  async LoadModels(): Promise<void> {
    const { meshes } = await SceneLoader.ImportMeshAsync(
      "",
      "./models/",
      "warehouse_v0.glb"
    );

    console.log("meshes", meshes);
  }

}