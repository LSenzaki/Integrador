# Database Setup Guide - Supabase

##  Overview
This guide will help you set up the PostgreSQL database schema in Supabase for the Facial Recognition Attendance System.

## 🗃 Database Structure

### Tables Created:
1. **`turmas`** - Classes (e.g., "IA 1º Ano", "Data Science 3º Ano")
2. **`professores`** - Professors with email and status
3. **`turmas_professores`** - Many-to-many relationship between professors and classes
4. **`alunos`** - Students with validation status and class assignment
5. **`face_embeddings`** - Face recognition embeddings (multiple photos per student)
6. **`presencas`** - Attendance records with confidence scores

### Additional Features:
-  **Indexes** for fast queries
-  **Auto-updating timestamps** (created_at, updated_at)
-  **Views** for common queries
-  **Stored function** for date-based attendance retrieval
-  **Sample data** included for testing

---

##  Setup Instructions

### Step 1: Access Supabase SQL Editor

1. Go to [https://supabase.com](https://supabase.com)
2. Log in to your account
3. Select your project (or create a new one)
4. Click on **"SQL Editor"** in the left sidebar

### Step 2: Run the Schema

1. Open the file: `backend/database_schema.sql`
2. Copy the entire contents
3. Paste into the Supabase SQL Editor
4. Click **"Run"** or press `Ctrl + Enter`
5. Wait for confirmation message: "Success. No rows returned"

### Step 3: Verify Tables

Go to **"Table Editor"** in the left sidebar and verify you see:
-  turmas
-  professores
-  turmas_professores
-  alunos
-  face_embeddings
-  presencas

### Step 4: Update Backend Configuration

Make sure your `backend/.env` file has the correct Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

You can find these in:
- Supabase Dashboard → Settings → API → Project URL
- Supabase Dashboard → Settings → API → Project API keys (anon/public)

---

##  Database Relationships

```
turmas (classes)
  ↓ 1:many
alunos (students)
  ↓ 1:many
face_embeddings (photos)

turmas ←→ turmas_professores ←→ professores
(many-to-many relationship)

alunos → presencas (attendances)
turmas → presencas
professores → presencas (validation)
```

---

##  Useful Views Created

### 1. `vw_alunos_completo`
Complete student information with class name and photo count
```sql
SELECT * FROM vw_alunos_completo;
```

### 2. `vw_professores_turmas`
Professors with their assigned classes as JSON
```sql
SELECT * FROM vw_professores_turmas;
```

### 3. `vw_presencas_completo`
Complete attendance information with all names
```sql
SELECT * FROM vw_presencas_completo WHERE data = CURRENT_DATE;
```

---

##  Useful Functions

### Get attendances by date:
```sql
SELECT * FROM get_presencas_by_date('2025-11-14');
```

---

##  Sample Queries

### Check all students in a class:
```sql
SELECT a.nome, a.check_professor, t.nome as turma
FROM alunos a
LEFT JOIN turmas t ON a.turma_id = t.id
WHERE t.nome = 'IA 1º Ano';
```

### Get today's attendances:
```sql
SELECT * FROM vw_presencas_completo 
WHERE DATE(data_hora) = CURRENT_DATE
ORDER BY data_hora DESC;
```

### Count attendances by student:
```sql
SELECT a.nome, COUNT(pr.id) as total_presencas
FROM alunos a
LEFT JOIN presencas pr ON a.id = pr.aluno_id
GROUP BY a.id, a.nome
ORDER BY total_presencas DESC;
```

### Find students pending professor validation:
```sql
SELECT nome FROM alunos WHERE check_professor = FALSE;
```

### Professor's classes:
```sql
SELECT p.nome as professor, t.nome as turma
FROM professores p
JOIN turmas_professores tp ON p.id = tp.professor_id
JOIN turmas t ON tp.turma_id = t.id;
```

---

##  Testing with Sample Data

The schema includes sample data:
- 3 classes (IA 1º Ano, Data Science 3º Ano, Machine Learning 2º Ano)
- 2 professors (Prof. Maria Santos, Prof. João Silva)
- 1 assignment (Prof. Maria → IA 1º Ano)

To add more test data:
```sql
-- Add a test student
INSERT INTO alunos (nome, turma_id, check_professor)
SELECT 'João Silva', id, TRUE
FROM turmas WHERE nome = 'IA 1º Ano';

-- Add a test attendance
INSERT INTO presencas (aluno_id, turma_id, confianca)
SELECT id, turma_id, 95.5
FROM alunos WHERE nome = 'João Silva';
```

---

##  Security Notes

- RLS (Row Level Security) is **commented out** by default
- Uncomment RLS policies if you add authentication later
- Current setup allows all operations (good for development)
- For production, enable RLS and create appropriate policies

---

##  Troubleshooting

### Error: "relation already exists"
- Tables already created. Either:
  - Skip the error and continue
  - Or run the cleanup script at the bottom of `database_schema.sql`

### Error: "permission denied"
- Make sure you're using the correct Supabase key
- Check that your project is active

### Slow queries?
- Indexes are already created
- For large datasets, consider adding more indexes based on your query patterns

---

## 🗑 Cleanup (Development Only)

To completely reset the database, run the cleanup script at the bottom of `database_schema.sql`:

```sql
-- Uncomment the DROP statements at the end of the schema file
-- WARNING: This deletes ALL data!
```

---

##  Next Steps

After database setup:
1.  Update FastAPI models to match the schema
2.  Create API endpoints for CRUD operations
3.  Test with the frontend
4.  Add data validation
5.  Implement facial recognition storage

---

## 📞 Support

If you encounter issues:
1. Check Supabase logs: Dashboard → Logs
2. Verify .env credentials
3. Test connection with a simple query
4. Check Supabase service status
