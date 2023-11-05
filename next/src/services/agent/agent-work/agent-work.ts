export default interface AgentWork {
  run: () => Promise<void>;
  conclude: () => Promise<void>;
  next: (data?: any) => AgentWork | undefined;
  onError: (e: unknown) => boolean; // Handles errors and returns whether to continue retrying
  getData: () => any;
}

// For each class that implements AgentWork, add the following method:
// getData(): any {
//   // Return any data that needs to be passed on to the next task.
// }

// In the AutonomousAgent class, modify the run() method as follows:
// async run() {
//   // existing code...
//   while (this.workLog[0]) {
//     // existing code...
//     const workData = this.workLog[0].getData();
//     const next = this.workLog[0].next(workData);
//     // existing code...
//   }
//   // existing code...
// }