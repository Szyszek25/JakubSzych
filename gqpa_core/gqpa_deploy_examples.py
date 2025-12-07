"""
💼 GQPA DIAMOND - CZĘŚĆ 9: DEPLOYMENT EXAMPLES
Praktyczne przykłady użycia
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║            💼 DEPLOYMENT EXAMPLES & USE CASES 💼                 ║
╚══════════════════════════════════════════════════════════════════╝
""")

# ============================================================================
# INICJALIZACJA DEPLOYMENT MANAGERA
# ============================================================================

print("\n[1] Inicjalizacja Deployment Managera...")
deploy = DeploymentManager(agent, adapter)

# ============================================================================
# PRZYKŁAD 1: SAVE & LOAD
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 1: SAVE & LOAD AGENT STATE")
print("="*70)

# Zapisz aktualny stan
print("\n📦 Zapisywanie agenta...")
checkpoint_path = deploy.quick_save()
print(f"✅ Checkpoint utworzony: {checkpoint_path}")

# Lista checkpointów
print("\n📋 Lista checkpointów:")
checkpoints = deploy.state_manager.list_checkpoints()

# Możesz wczytać później:
# deploy.quick_load("checkpoint_20250120_143022.pkl")

# ============================================================================
# PRZYKŁAD 2: REST API SIMULATION
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 2: REST API REQUESTS")
print("="*70)

# Symulacja różnych requestów API
api_requests = [
    {
        "action": "status",
        "data": {}
    },
    {
        "action": "goal",
        "data": {"goal": "optimize learning efficiency"}
    },
    {
        "action": "cycle",
        "data": {"cycles": 10}
    }
]

print("\n🌐 Przetwarzanie requestów API...")
api_responses = []

for i, request in enumerate(api_requests, 1):
    print(f"\n   Request {i}/{len(api_requests)}: {request['action']}")
    response = deploy.api_wrapper.process_request(request)
    api_responses.append(response)
    
    if response['success']:
        print(f"   ✅ Success (time: {response['processing_time_ms']:.2f}ms)")
    else:
        print(f"   ❌ Error: {response.get('error', 'Unknown')}")

# Statystyki API
api_stats = deploy.api_wrapper.get_api_stats()
print(f"\n📊 API Statistics:")
print(f"   Total requests: {api_stats['total_requests']}")
print(f"   Requests/min: {api_stats['requests_per_minute']:.2f}")

# ============================================================================
# PRZYKŁAD 3: BATCH PROCESSING
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 3: BATCH PROCESSING")
print("="*70)

print("\n📦 Tworzenie batch jobs...")

# Dodaj różne zadania
deploy.batch_processor.add_job(
    'goal', 
    {'goal': 'explore new environment'}, 
    priority=10
)

deploy.batch_processor.add_job(
    'cycles', 
    {'cycles': 20}, 
    priority=8
)

deploy.batch_processor.add_job(
    'goal', 
    {'goal': 'maximize creativity'}, 
    priority=7
)

deploy.batch_processor.add_job(
    'cycles', 
    {'cycles': 15}, 
    priority=6
)

deploy.batch_processor.add_job(
    'analysis', 
    {}, 
    priority=5
)

# Przetwórz wszystkie
print("\n🔄 Processing batch...")
results = deploy.batch_processor.process_batch()

# Podsumowanie
summary = deploy.batch_processor.get_summary()
print(f"\n📊 Batch Summary:")
print(f"   Completed: {summary['completed']}/{summary['total_jobs']}")
print(f"   Success rate: {summary['success_rate']*100:.1f}%")
print(f"   Avg time: {summary['avg_processing_time']*1000:.2f}ms")

# ============================================================================
# PRZYKŁAD 4: MONITORING
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 4: PRODUCTION MONITORING")
print("="*70)

print("\n📈 Zbieranie metryk...")

# Zbieraj metryki przez kilka cykli
for i in range(5):
    # Wykonaj kilka cykli
    for _ in range(10):
        agent.cognitive_cycle()
    
    # Zbierz metryki
    metrics = deploy.monitor.collect_metrics()
    print(f"   Cycle {agent.cycle_count}: Learning={metrics['learning_progress']*100:.1f}%, Chaos={metrics['chaos_level']:.3f}")

# Generuj raport
print("\n📋 Generowanie raportu monitoringu...")
report = deploy.monitor.generate_report()

# ============================================================================
# PRZYKŁAD 5: FULL STATUS CHECK
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 5: FULL DEPLOYMENT STATUS")
print("="*70)

status = deploy.full_status()

# ============================================================================
# PRZYKŁAD 6: PRODUCTION WORKFLOW
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 6: TYPICAL PRODUCTION WORKFLOW")
print("="*70)

def production_workflow():
    """Typowy workflow produkcyjny"""
    
    print("\n🔄 Starting production workflow...")
    
    # 1. Health check
    print("\n[1/5] Health check...")
    health = deploy.health_check()
    print(f"   Status: {health}")
    
    if health == "DEGRADED":
        print("   ⚠️ System degraded, loading last checkpoint...")
        checkpoints = deploy.state_manager.list_checkpoints()
        if checkpoints:
            deploy.quick_load(checkpoints[-1])
    
    # 2. Process new goal
    print("\n[2/5] Setting production goal...")
    goal_request = {
        "action": "goal",
        "data": {"goal": "maximize task completion efficiency"}
    }
    response = deploy.api_wrapper.process_request(goal_request)
    print(f"   Goal set: {response['result']['new_goal']}")
    
    # 3. Execute cycles
    print("\n[3/5] Executing cognitive cycles...")
    cycle_request = {
        "action": "cycle",
        "data": {"cycles": 50}
    }
    response = deploy.api_wrapper.process_request(cycle_request)
    print(f"   Cycles completed: {response['result']['cycles_executed']}")
    
    # 4. Collect metrics
    print("\n[4/5] Collecting metrics...")
    metrics = deploy.monitor.collect_metrics()
    print(f"   Learning: {metrics['learning_progress']*100:.1f}%")
    print(f"   Objects: {metrics['world_objects']}")
    print(f"   Episodes: {metrics['episodes']}")
    
    # 5. Save checkpoint
    print("\n[5/5] Creating checkpoint...")
    checkpoint = deploy.quick_save()
    print(f"   Checkpoint saved: {checkpoint}")
    
    print("\n✅ Workflow completed successfully!")
    
    return {
        'health': health,
        'metrics': metrics,
        'checkpoint': checkpoint
    }

# Uruchom workflow
workflow_result = production_workflow()

# ============================================================================
# PRZYKŁAD 7: LONG-RUNNING SERVICE
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 7: LONG-RUNNING SERVICE SIMULATION")
print("="*70)

def simulate_long_running_service(duration_seconds=30):
    """Symuluje długo działającą usługę"""
    
    print(f"\n🚀 Starting service for {duration_seconds}s...")
    
    start_time = time.time()
    cycle_count = 0
    checkpoint_interval = 10  # Checkpoint co 10s
    last_checkpoint = start_time
    
    while time.time() - start_time < duration_seconds:
        # Cognitive cycle
        agent.cognitive_cycle()
        cycle_count += 1
        
        # Health check co 5 cykli
        if cycle_count % 5 == 0:
            health = deploy.health_check()
            if health != "HEALTHY":
                print(f"   ⚠️ Health: {health}")
        
        # Checkpoint co 10s
        if time.time() - last_checkpoint > checkpoint_interval:
            deploy.quick_save()
            last_checkpoint = time.time()
            print(f"   💾 Checkpoint at {cycle_count} cycles")
        
        # Small delay
        time.sleep(0.1)
    
    print(f"\n✅ Service ran for {duration_seconds}s")
    print(f"   Cycles executed: {cycle_count}")
    print(f"   Final learning: {agent.emergent_integrator.get_integration_status()['emergent_metrics']['learning_progress']*100:.1f}%")

# Uruchom krótką symulację (10s)
print("\n🔧 Running 10-second simulation...")
simulate_long_running_service(10)

# ============================================================================
# PRZYKŁAD 8: EXPORT FOR CLOUD DEPLOYMENT
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 8: EXPORT FOR CLOUD DEPLOYMENT")
print("="*70)

def export_for_cloud():
    """Przygotuj agenta do cloud deployment"""
    
    print("\n☁️ Preparing for cloud deployment...")
    
    # 1. Create production checkpoint
    print("\n[1/4] Creating production checkpoint...")
    checkpoint = deploy.state_manager.save_agent(
        "agent_production_v1.0.pkl",
        compress=True
    )
    
    # 2. Export configuration
    print("\n[2/4] Exporting configuration...")
    config = {
        'version': '1.0.0',
        'model': 'HAMA2-Cognitive',
        'checkpoint_file': 'agent_production_v1.0.pkl.gz',
        'api_endpoint': '/api/v1/agent',
        'health_check': '/health',
        'metrics': {
            'learning_progress': agent.emergent_integrator.get_integration_status()['emergent_metrics']['learning_progress'],
            'total_cycles': agent.cycle_count,
            'world_objects': len(agent.world_model.objects)
        }
    }
    
    with open('/content/checkpoints/deployment_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("   ✅ Config saved: deployment_config.json")
    
    # 3. Create requirements.txt
    print("\n[3/4] Creating requirements.txt...")
    requirements = [
        "torch>=2.0.0",
        "google-generativeai>=0.3.0",
        "numpy>=1.24.0",
        "cloudpickle>=2.2.0",
        "tqdm>=4.65.0"
    ]
    
    with open('/content/checkpoints/requirements.txt', 'w') as f:
        f.write('\n'.join(requirements))
    
    print("   ✅ Requirements saved")
    
    # 4. Create deployment script
    print("\n[4/4] Creating deployment script...")
    deployment_script = '''#!/usr/bin/env python3
"""
Production Deployment Script
Auto-generated by GQPA Diamond
"""

import cloudpickle
import gzip

def load_agent(checkpoint_path):
    with gzip.open(checkpoint_path, 'rb') as f:
        state = cloudpickle.load(f)
    return state

def main():
    print("Loading agent...")
    state = load_agent("agent_production_v1.0.pkl.gz")
    print(f"Agent loaded - Learning: {state['metadata']['learning_progress']*100:.1f}%")
    # Add your deployment logic here

if __name__ == "__main__":
    main()
'''
    
    with open('/content/checkpoints/deploy.py', 'w') as f:
        f.write(deployment_script)
    
    print("   ✅ Deployment script saved")
    
    print("\n✅ Cloud deployment package ready!")
    print("\n📦 Package contents:")
    print("   - agent_production_v1.0.pkl.gz (agent checkpoint)")
    print("   - deployment_config.json (configuration)")
    print("   - requirements.txt (dependencies)")
    print("   - deploy.py (deployment script)")
    
    return config

cloud_config = export_for_cloud()

# ============================================================================
# PRZYKŁAD 9: DOWNLOAD FILES (for local deployment)
# ============================================================================

print("\n" + "="*70)
print("PRZYKŁAD 9: DOWNLOAD FILES")
print("="*70)

print("\n💾 Przygotowanie plików do pobrania...")

from google.colab import files

def download_deployment_package():
    """Pobierz wszystkie pliki deployment"""
    
    print("\n📥 Downloading deployment files...")
    print("   (Files will appear in your Downloads folder)")
    
    try:
        # Download checkpoint
        files.download('/content/checkpoints/agent_production_v1.0.pkl.gz')
        print("   ✅ agent_production_v1.0.pkl.gz")
        
        # Download config
        files.download('/content/checkpoints/deployment_config.json')
        print("   ✅ deployment_config.json")
        
        # Download requirements
        files.download('/content/checkpoints/requirements.txt')
        print("   ✅ requirements.txt")
        
        # Download deploy script
        files.download('/content/checkpoints/deploy.py')
        print("   ✅ deploy.py")
        
        # Download GQPA report
        files.download('/content/gqpa_diamond_report.json')
        print("   ✅ gqpa_diamond_report.json")
        
        print("\n✅ All files downloaded!")
        
    except Exception as e:
        print(f"   ⚠️ Download error: {e}")
        print("   Files are available in /content/checkpoints/")

print("\n🔽 Ready to download!")
print("   Uncomment and run: download_deployment_package()")

# Uncomment to download:
# download_deployment_package()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*70)
print("🎉 DEPLOYMENT SYSTEM READY!")
print("="*70)

print("\n📊 System Status:")
final_status = deploy.full_status()

print("\n✅ Available Commands:")
print("   deploy.quick_save()                    # Save checkpoint")
print("   deploy.quick_load('checkpoint.pkl')    # Load checkpoint")
print("   deploy.health_check()                  # Check health")
print("   deploy.full_status()                   # Full status")
print("   deploy.api_wrapper.process_request()   # Process API request")
print("   deploy.batch_processor.add_job()       # Add batch job")
print("   deploy.monitor.collect_metrics()       # Collect metrics")

print("\n📚 Next Steps:")
print("   1. Download deployment files")
print("   2. Deploy to your server/cloud")
print("   3. Set up monitoring")
print("   4. Configure auto-checkpointing")

print("\n" + "="*70)
print("Happy Deploying! 🚀")
print("="*70)
