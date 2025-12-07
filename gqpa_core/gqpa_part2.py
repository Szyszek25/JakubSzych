"""
🧠 GQPA DIAMOND - CZĘŚĆ 2: HAMA2 CORE ARCHITECTURE
Gotowe do wklejenia w Google Colab
"""

# ============================================================================
# KONFIGURACJA HAMA2
# ============================================================================

class HAMA2CognitiveConfig:
    def __init__(self):
        self.vocab_size = 512
        self.hidden_size = 384
        self.stochastic_units = 192
        self.lstm_layers = 4
        self.attention_heads = 8
        self.memory_size = 200
        self.initial_chaos = 0.15
        self.adaptation_rate = 0.02
        self.initial_memory_influence = 0.15
        self.cognitive_embedding_size = 384
        self.modality_channels = 5
        self.emotion_channels = 5
        self.chaos_range = (0.05, 0.4)
        self.memory_influence_range = (0.0, 0.4)
        self.learning_rate = 0.001
        self.weight_decay = 0.01
        self.dropout_rate = 0.1

print("✅ HAMA2 Config zdefiniowana")

# ============================================================================
# HAMA2 COGNITIVE CORE
# ============================================================================

class HAMA2CognitiveCore(nn.Module):
    def __init__(self, config: HAMA2CognitiveConfig):
        super().__init__()
        self.config = config

        # Embeddings
        self.cognitive_embedding = nn.Embedding(config.vocab_size, config.hidden_size)
        self.modality_embeddings = nn.ModuleDict({
            'vision': nn.Linear(100, config.hidden_size),
            'audio': nn.Linear(50, config.hidden_size),
            'language': nn.Linear(200, config.hidden_size),
            'proprioception': nn.Linear(30, config.hidden_size)
        })

        self.embedding_projection = nn.Linear(config.hidden_size, config.hidden_size)

        # LSTM Core
        self.lstm = nn.LSTM(
            config.hidden_size,
            config.hidden_size,
            config.lstm_layers,
            batch_first=True,
            dropout=config.dropout_rate
        )

        # Emergent Encoder
        self.emergent_encoder = nn.Sequential(
            nn.Linear(config.stochastic_units * 2, config.hidden_size),
            nn.LeakyReLU(0.1),
            nn.LayerNorm(config.hidden_size),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.Tanh()
        )

        # Attention
        self.cognitive_attention = nn.MultiheadAttention(
            config.hidden_size,
            config.attention_heads,
            batch_first=True,
            dropout=0.1
        )

        # Memory
        self.memory_network = nn.GRUCell(config.hidden_size, config.hidden_size)
        self.memory_buffers = {}

        # Output
        self.cognitive_output = nn.Sequential(
            nn.Linear(config.hidden_size * 2, config.hidden_size),
            nn.LeakyReLU(0.1),
            nn.LayerNorm(config.hidden_size),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.hidden_size, config.vocab_size)
        )

        self._init_emergent_state()
        self._initialize_weights()

    def _init_emergent_state(self):
        self.register_buffer('emergent_state', torch.zeros(1))
        self.register_buffer('chaos_level', torch.tensor(self.config.initial_chaos))
        self.register_buffer('learning_progress', torch.zeros(1))
        self.register_buffer('memory_influence', torch.tensor(self.config.initial_memory_influence))
        self.performance_history = deque(maxlen=100)
        self.cognitive_complexity = 0.5
        self.adaptation_speed = 1.0

    def _initialize_weights(self):
        for name, param in self.named_parameters():
            if 'weight' in name and param.dim() >= 2:
                if 'lstm' in name:
                    nn.init.orthogonal_(param)
                elif 'attention' in name:
                    nn.init.xavier_uniform_(param)
                else:
                    nn.init.kaiming_uniform_(param, nonlinearity='leaky_relu')
            elif 'bias' in name:
                nn.init.constant_(param, 0.1)

    def _get_memory_buffer(self, batch_size: int):
        if batch_size not in self.memory_buffers:
            self.memory_buffers[batch_size] = deque(maxlen=self.config.memory_size)
        return self.memory_buffers[batch_size]

    def _generate_emergent_context(self, batch_size: int, seq_len: int, 
                                   device: torch.device, cognitive_context: torch.Tensor = None):
        base_noise = torch.randn(batch_size, seq_len, self.config.stochastic_units, device=device) * 0.1
        state_influence = torch.sigmoid(self.emergent_state * 2 - 1)
        adaptive_noise = base_noise * (0.2 + state_influence * 0.3)
        
        chaos_vector = torch.ones(batch_size, seq_len, self.config.stochastic_units, device=device)
        chaos_vector = chaos_vector * torch.sigmoid(self.chaos_level * 3 - 1) * 0.3
        
        combined_input = torch.cat([adaptive_noise, chaos_vector], dim=-1)
        emergent_context = self.emergent_encoder(combined_input)
        
        if cognitive_context is not None:
            emergent_context = emergent_context + cognitive_context * 0.1
        
        return emergent_context

    def _update_cognitive_memory(self, hidden_states: list, batch_size: int, 
                                cognitive_context: Dict[str, Any] = None):
        if not hidden_states:
            return
        
        memory_buffer = self._get_memory_buffer(batch_size)
        recent_hidden = hidden_states[-1].mean(dim=1)
        
        if len(memory_buffer) == 0:
            memory_state = torch.zeros_like(recent_hidden)
        else:
            memory_state = memory_buffer[-1]
        
        new_memory = self.memory_network(recent_hidden, memory_state)
        memory_buffer.append(new_memory.detach())

    def _get_cognitive_memory_context(self, batch_size: int, device: torch.device):
        memory_buffer = self._get_memory_buffer(batch_size)
        if len(memory_buffer) == 0:
            return torch.zeros(batch_size, self.config.hidden_size, device=device)
        
        recent_memories = list(memory_buffer)[-3:]
        memory_tensor = torch.stack(recent_memories)
        return memory_tensor.mean(dim=0)

    def forward(self, x: torch.Tensor = None, cognitive_data: Dict[str, Any] = None,
                hidden: Optional[Tuple] = None, force_deterministic: bool = False):
        if x is None and cognitive_data is None:
            raise ValueError("Either x or cognitive_data must be provided")

        batch_size = 1
        seq_len = 1
        device = next(self.parameters()).device

        cognitive_embedding = None
        if cognitive_data is not None:
            cognitive_embedding = self._encode_cognitive_input(cognitive_data)
            seq_len = cognitive_embedding.shape[1]

        if x is not None:
            x_embed = self.cognitive_embedding(x)
            x_embed = self.embedding_projection(x_embed)
            batch_size, seq_len = x.shape
        else:
            x_embed = cognitive_embedding if cognitive_embedding is not None else torch.zeros(
                batch_size, seq_len, self.config.hidden_size, device=device)

        lstm_out, hidden = self.lstm(x_embed, hidden)

        if self.training:
            self._update_cognitive_memory([lstm_out], batch_size, cognitive_data)

        if not force_deterministic and self.training:
            emergent_context = self._generate_emergent_context(
                batch_size, seq_len, device, cognitive_embedding)
            lstm_out = lstm_out + emergent_context * self.chaos_level * 0.4

        attended, _ = self.cognitive_attention(lstm_out, lstm_out, lstm_out)
        lstm_out = lstm_out + attended * 0.4

        memory_context = self._get_cognitive_memory_context(batch_size, device)
        memory_context = memory_context.unsqueeze(1).expand(-1, seq_len, -1)
        lstm_out = lstm_out + memory_context * self.memory_influence

        if cognitive_embedding is not None:
            cognitive_context = cognitive_embedding.expand(batch_size, seq_len, -1)
            integrated_features = torch.cat([lstm_out, cognitive_context], dim=-1)
        else:
            integrated_features = torch.cat([lstm_out, memory_context], dim=-1)

        output = self.cognitive_output(integrated_features)
        return output, hidden

    def _encode_cognitive_input(self, cognitive_data: Dict[str, Any]) -> torch.Tensor:
        modality_embeddings = []
        device = next(self.parameters()).device

        if 'perception' in cognitive_data:
            for modality_data in cognitive_data['perception']:
                modality_type = str(modality_data.get('modality', 'unknown')).lower()
                if 'vision' in modality_type:
                    features = torch.randn(100, device=device)
                    embedding = self.modality_embeddings['vision'](features)
                    modality_embeddings.append(embedding)
                elif 'audio' in modality_type:
                    features = torch.randn(50, device=device)
                    embedding = self.modality_embeddings['audio'](features)
                    modality_embeddings.append(embedding)

        if modality_embeddings:
            combined_modality = torch.stack(modality_embeddings).mean(dim=0)
        else:
            combined_modality = torch.zeros(self.config.hidden_size, device=device)
        
        return combined_modality.unsqueeze(0).unsqueeze(0)

    def update_emergent_state(self, outputs: torch.Tensor = None, targets: torch.Tensor = None,
                            loss: float = None, cognitive_feedback: Dict[str, Any] = None):
        with torch.no_grad():
            if outputs is not None and targets is not None:
                predictions = torch.argmax(outputs, dim=-1)
                accuracy = (predictions == targets).float().mean()
                self.performance_history.append(accuracy.item())
            else:
                accuracy = torch.tensor(0.5)

            if cognitive_feedback:
                goal_progress = cognitive_feedback.get('goal_progress', 0.5)
                emotional_arousal = cognitive_feedback.get('emotional_arousal', 0.5)
                novelty = cognitive_feedback.get('novelty', 0.5)
            else:
                goal_progress, emotional_arousal, novelty = 0.5, 0.5, 0.5

            cognitive_factor = (goal_progress + emotional_arousal + novelty) / 3.0
            target_accuracy = 0.4 + cognitive_factor * 0.3
            accuracy_error = target_accuracy - accuracy.item()

            if len(self.performance_history) >= 5:
                performance_trend = np.mean(list(self.performance_history)[-5:])
            else:
                performance_trend = accuracy.item()

            adaptation_rate = self.config.adaptation_rate * (0.3 + performance_trend * 0.7)
            chaos_update = adaptation_rate * accuracy_error * 0.2
            chaos_update += novelty * 0.05 - goal_progress * 0.02
            new_chaos = self.chaos_level + chaos_update
            new_chaos = torch.clamp(new_chaos, *self.config.chaos_range)

            state_momentum = 0.9
            state_update = torch.tanh(accuracy - target_accuracy) * 0.1
            state_update += emotional_arousal * 0.05 - 0.025
            new_state = state_momentum * self.emergent_state + (1 - state_momentum) * state_update

            if loss is not None:
                progress_update = -loss * 0.001 + accuracy * 0.01 + goal_progress * 0.005
            else:
                progress_update = accuracy * 0.01 + goal_progress * 0.005
            new_progress = torch.clamp(self.learning_progress + progress_update, 0, 1)

            memory_update = accuracy * 0.01 - (loss if loss else 0) * 0.005 + novelty * 0.01
            new_memory_influence = torch.clamp(
                self.memory_influence + memory_update,
                *self.config.memory_influence_range
            )

            complexity_update = novelty * 0.1 + (1 - goal_progress) * 0.05
            self.cognitive_complexity = 0.95 * self.cognitive_complexity + 0.05 * complexity_update

            self.chaos_level.copy_(new_chaos)
            self.emergent_state.copy_(new_state)
            self.learning_progress.copy_(new_progress)
            self.memory_influence.copy_(new_memory_influence)

    def get_emergent_metrics(self) -> Dict[str, float]:
        return {
            'chaos_level': self.chaos_level.item(),
            'emergent_state': self.emergent_state.item(),
            'learning_progress': self.learning_progress.item(),
            'memory_influence': self.memory_influence.item(),
            'cognitive_complexity': self.cognitive_complexity,
            'performance_trend': np.mean(list(self.performance_history)) if self.performance_history else 0.0,
            'adaptation_speed': self.adaptation_speed
        }

    def reset_memory(self, batch_size: Optional[int] = None):
        if batch_size is None:
            self.memory_buffers.clear()
        elif batch_size in self.memory_buffers:
            del self.memory_buffers[batch_size]

print("✅ HAMA2 Core zdefiniowany")
print("\n" + "="*70)
print("CZĘŚĆ 2 ZAKOŃCZONA - Przejdź do CZĘŚCI 3")
print("="*70)
