import type { StateCreator } from "zustand";
import { create } from "zustand";

import { createSelectors } from "./helpers";
import type { Message } from "../types/message";
import type { Task } from "../types/task";
import { isTask, TASK_STATUS_COMPLETED, TASK_STATUS_EXECUTING } from "../types/task";

export const isExistingTask = (message: Message): boolean =>
  isTask(message) &&
  (message.status === TASK_STATUS_EXECUTING || message.status === TASK_STATUS_COMPLETED);

const resetters: (() => void)[] = [];

const initialTaskState = {
  tasks: [],
};

export interface TaskSlice {
  tasks: Task[];
  addTask: (newTask: Task) => void;
  updateTask: (updatedTask: Task) => void;
  deleteTask: (taskId: string) => void;
  updateTaskResult: (taskId: string, result: string) => void;
}

export const createTaskSlice: StateCreator<TaskSlice, [], [], TaskSlice> = (set) => {
  resetters.push(() => set(initialTaskState));

  return {
    ...initialTaskState,
    addTask: (newTask) => {
      set((state) => {
        const tasks = [...state.tasks];
        const parentTaskIndex = tasks.findIndex(task => task.taskId === newTask.parentTaskId);
        tasks.splice(parentTaskIndex + 1, 0, { ...newTask });
        return {
          ...state,
          tasks,
        };
      });
    },
    updateTask: (updatedTask) => {
      set((state) => {
        const updatedTasks = state.tasks.map((task) => {
          if (task.id === updatedTask.id && task.taskId == updatedTask.taskId) {
            return {
              ...updatedTask,
            };
          }
          return task;
        });

        return {
          ...state,
          tasks: updatedTasks,
        };
      });
    },
    deleteTask: (taskId) => {
      set((state) => ({
        ...state,
        tasks: state.tasks.filter((task) => task.taskId !== taskId),
      }));
    },
    updateTaskResult: (taskId, result) => {
      set((state) => ({
        ...state,
        tasks: state.tasks.map((task) => {
          if (task.taskId === taskId) {
            return { ...task, result };
          }
          return task;
        }),
      }));
    },
  };
};

export const useTaskStore = createSelectors(
  create<TaskSlice>()((...a) => ({
    ...createTaskSlice(...a),
  }))
);

export const resetAllTaskSlices = () => resetters.forEach((resetter) => resetter());