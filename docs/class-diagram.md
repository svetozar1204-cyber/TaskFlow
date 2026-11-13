
classDiagram
    class Project {
        +int id
        +string name
        +text description
        +datetime created_at
        +List~Task~ tasks
        +repr()
    }

    class Task {
        +int id
        +string title
        +text description
        +string status
        +date due_date
        +datetime created_at
        +int project_id
        +Project project
        +repr()
    }

    Project "1" --> "0..*" Task : contains
