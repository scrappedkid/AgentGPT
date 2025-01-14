import { v4 } from "uuid";

import { useAgentStore } from "../../stores";
import { useTaskStore } from "../../stores/taskStore";
import type { Task, TaskStatus } from "../../types/task";

/*
 * Abstraction over model used by Autonomous Agent to encapsulate the data required for a given run
 */
export interface AgentRunModel {
  getId(): string;

  getGoal(): string;

  getLifecycle(): AgentLifecycle;

  setLifecycle(AgentLifecycle): void;

  getRemainingTasks(): Task[];

  getCurrentTask(): Task | undefined;

  updateTaskStatus(task: Task, status: TaskStatus): Task;

  updateTaskResult(task: Task, result: string): Task;

  getCompletedTasks(): Task[];

  addTask(taskValue: string, parentTaskId?: string): void;

  removeTask(task: Task): void;

  updateTask(task: Task): Task;
}


export type AgentLifecycle = "offline" | "running" | "pausing" | "paused" | "stopped";

export class DefaultAgentRunModel implements AgentRunModel {
  private readonly id: string;
  private readonly goal: string;
  tasks: any;

  constructor(goal: string) {
    this.id = v4().toString();
    this.goal = goal;
  }
  getCurrentTask() {
    throw new Error("Method not implemented.");
  }


    getId = () => this.id;

  getGoal = () => this.goal;
  getLifecycle = (): AgentLifecycle => useAgentStore.getState().lifecycle;
  setLifecycle = (lifecycle: AgentLifecycle) => useAgentStore.getState().setLifecycle(lifecycle);

  getRemainingTasks = (): Task[] => {
    return useTaskStore.getState().tasks.filter((t: Task) => t.status === "started");
  };

  addTask = (taskValue: string, parentTaskId?: string): void => {
    useTaskStore.getState().addTask({
      id: v4().toString(),
      type: "task",
      value: taskValue,
      status: "started",
      result: "",
      parentTaskId,
    });
  };


  removeTask = (task: Task): void => {
    const taskIndex = this.tasks.findIndex((t) => t.id === task.id);
    if (taskIndex > -1) {
      this.tasks.splice(taskIndex, 1);
    }
  };

  updateTaskStatus(task: Task, status: TaskStatus): Task {
    return this.updateTask({ ...task, status });
  }

  updateTaskResult(task: Task, result: string): Task {
    return this.updateTask({ ...task, result });
  }

  updateTask = (task: Task): Task => {
    const taskIndex = this.tasks.findIndex((t) => t.id === task.id);
    if (taskIndex > -1) {
      this.tasks[taskIndex] = task;
    }
    return task;
  };
}
