// next/src/services/agent/data-store.tsx

export interface DataStore {
  setData(key: string, value: any): void;
  getData(key: string): any;
}

export class DefaultDataStore implements DataStore {
  private data: Record<string, any> = {};
  
  setData(key: string, value: any): void {
    this.data[key] = value;
  }
  
  getData(key: string): any {
    return this.data[key];
  }
}

// next/src/services/agent/agent-run-model.tsx

export interface AgentRunModel {
  // existing methods...
  getDataStore(): DataStore;
}

export class DefaultAgentRunModel implements AgentRunModel {
  private dataStore: DataStore = new DefaultDataStore();
  // existing methods...
  
  getDataStore(): DataStore {
    return this.dataStore;
  }
}