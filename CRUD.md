# 🔨 Implementação do CRUD

O projeto implementa operações CRUD seguindo o padrão MVT (Model-View-Template) do Django, com funcionalidades distribuídas em 4 apps principais.

### > Estrutura do CRUD

- **Models** (`apps/*/models.py`): Definem a estrutura dos dados e lógica de negócio
- **Views** (`apps/*/views.py`): Processam requisições HTTP e implementam a lógica CRUD
- **Forms** (`apps/*/forms.py`): Validam dados e gerenciam entrada do usuário
- **Templates** (`templates/*/`): Renderizam HTML para a interface
- **URLs** (`apps/*/urls.py`): Mapeiam URLs para views

---

### > Principais Operações CRUD

#### 1. **Places (Lugares Turísticos)** - CRUD Completo

- **CREATE**

  - `place_create_view`: Usuários autenticados podem criar lugares com múltiplas imagens.
  - Usa **formsets** para upload de múltiplas imagens.
  - Lugares começam como **não aprovados** (`is_approved=False`).

- **READ**

  - `explore_view`: Lista todos os lugares aprovados com busca.
  - `place_detail_view`: Mostra detalhes do lugar com reviews, imagens e mapa.
  - `category_detail_view`: Exibe lugares por categoria.

- **UPDATE**

  - `place_update_view`: Dono ou admin pode editar.
  - Gerencia múltiplas imagens via **formset**.

- **DELETE**
  - `place_delete_view`: Dono ou admin pode deletar.
  - Requer confirmação antes da exclusão.

---

#### 2. **Sistema de Aprovação**

- `approval_queue_view`: Fila de lugares pendentes (**admin**).
- `approve_place_view`: Aprovar lugar (**admin**).
- `reject_place_view`: Rejeitar lugar com motivo (**admin**).
- `backlog_view`: Exibe todos os lugares com filtros (**admin**).

---

#### 3. **Reviews (Avaliações)** — CRUD Completo

- `review_create_view`: Usuários podem avaliar lugares (1 review por usuário para cada lugar).
- `place_detail_view`: Exibe todas as avaliações do lugar.
- `review_edit_view`: Dono ou admin pode editar uma avaliação.
- `review_delete_view`: Dono ou admin pode deletar uma avaliação.

---

#### 4. **Favorites (Favoritos)** — Sistema de Toggle

- `toggle_favorite_view`: Endpoint **AJAX** para adicionar ou remover favoritos.
- Usuários autenticados sincronizam com o backend.
- `favorites_list_view`: Lista de favoritos do usuário.
- `sync_favorites_view`: Sincroniza `localStorage` com o backend.

---

#### 5. **Users (Usuários)** — Gerenciamento Admin

- `register_view`: Registro público com suporte a **Google OAuth**.
- `user_management_view`: Lista usuários (**admin only**).
- `user_update_type_view`: Atualiza permissões (**admin**).
- `user_toggle_status_view`: Ativa ou desativa usuários (**admin**).
- `user_delete_view`: Deleta usuários (**admin**).

---

#### 6. **News / Events (Notícias e Eventos)** — Somente Leitura

- `news_list_view`: Lista notícias e eventos.
- `news_detail_view`: Exibe detalhes com contador de visualizações.

---

#### **CRUD completo via Django Admin**

- Criação, edição e exclusão disponíveis apenas para administradores.

---

### Sistema de Permissões

| Funcionalidade           | Autenticado | Admin/Staff |
| ------------------------ | ----------- | ----------- |
| Ver lugares aprovados    | ✅          | ✅          |
| Ver lugares pendentes    | Próprios    | ✅          |
| Criar lugares            | ✅          | ✅          |
| Editar próprios lugares  | ✅          | ✅          |
| Avaliar lugares          | ✅          | ✅          |
| Favoritar (localStorage) | ✅          | ✅          |
| Editar qualquer lugar    | ❌          | ✅          |
| Aprovar/Rejeitar         | ❌          | ✅          |
| Gerenciar usuários       | ❌          | ✅          |
